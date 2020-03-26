# Dublin Bike data analyzer

This app peridically fetches data from dublinbikes API and saves it into S3. It allows to visualise the data using local EK stack

Structure:
* dublinbike-data-fetcher - serverless app that fetches data and stores in S3
* local-data-visualisation - local ES and Kibana stack that feches the data and visualize it