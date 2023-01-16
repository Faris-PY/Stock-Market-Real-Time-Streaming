import json
import pandas as pd
from yahoo_fin import stock_info as si
import asyncio
from datetime import datetime
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from azure.identity import DefaultAzureCredential

EVENT_HUB_FULLY_QUALIFIED_NAMESPACE = "StockMarketEventHubNamespace"
EVENT_HUB_NAME = "stockmarkethub"

credential = DefaultAzureCredential()

def get_stock_data(stock):
    stockRaw = si.get_quote_data(stock)
    stock_df = pd.DataFrame([stockRaw], columns=stockRaw.keys())[['symbol', 'quoteType', 'market', 'exchangeTimezoneName',
                                                                'currency', 'marketState', 'regularMarketPrice', 'regularMarketTime',
                                                                 'marketCap', 'exchange', 'averageAnalystRating']]
    stock_df['regularMarketTime'] = datetime.fromtimestamp(stock_df['regularMarketTime'])
    stock_df['regularMarketTime'] = stock_df['regularMarketTime'].astype(str)
    stock_df[['AnalystRating', 'AnalystBuySell']] = stock_df['averageAnalystRating'].str.split('-', 1, expand=True)

    stock_df.drop('averageAnalystRating', axis=1, inplace=True)
    stock_df['MarketCapInTrillion$$'] = stock_df.apply(lambda row: "$" + str(round(row['marketCap']/1000000000000, 2)) + "MM", axis=1)
    stock_df.rename(columns= {'symbol': 'stock', 'exchangeTimezoneName': 'exchangeTimezone'}, inplace=True)
    return stock_df.to_dict('records')


async def run():
    while True: 
        await asyncio.sleep(5)
        producer = EventHubProducerClient(
        fully_qualified_namespace=EVENT_HUB_FULLY_QUALIFIED_NAMESPACE,
        eventhub_name=EVENT_HUB_NAME,
        credential=credential,
        )
        async with producer:
            event_data_batch = await producer.create_batch()

            event_data_batch.add(EventData(json.dumps(get_stock_data('GOOGL'))))

            await producer.send_batch(event_data_batch)
            print('data send')

            await credential.close()

loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(run())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing the loop")
    loop.close()
