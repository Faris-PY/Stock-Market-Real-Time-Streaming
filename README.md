# Stock-Market-Real-Time-Streaming
Azure Data Engineering

![Architecture diagram](https://user-images.githubusercontent.com/107489749/212629280-edf697ce-8d8f-477a-a146-a3c6af01cd9d.png)


## Resources used 
1. Azure Event Hubs
2. Azure Stream Analytics
3. Azure Synapse Analytics
4. Datalake Gen2
5. Data Factory
6. Power BI  


## Data flow step
1. Stock Simulation python App will fetch the details of a stock (ex. Gooogle[GOOGL]) in real time & send to Azure Event Hubs in json format.
2. Azure Event Hubs direct the messages to Azure Stream Analytics & capture that raw data into ADLS.
3. Azure Stream Analytics will query certain data from that message and insert into Azure Synapse Analytics, streamed into Power BI as a realtime dashboard.
4. Data from Synapse Analytics will moved to cool tier of ADLS once in 3 months using Azure Data Factory pileline.
5. Once the storage time of data crossess 7 months, it move be moved to achieve tier by Life Cycle Management.


## Functionalities covered as part of This project
1. Stream processing, Role Based Access
2. Event Hub - Capture Feature, Connectioing external python application with Event Hub
3. Stream Analytics - Multiple output in query, Streaming & Troubleshooting resouse log(diagnostics log), integration of Power BI
4. Data Factory - Schedule Event trigger, Linked service.
5. Datalake Gen2 - Lifecycle management.
