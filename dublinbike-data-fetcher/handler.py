import json
import requests
import boto3
import os
from datetime import datetime, timezone

# TODO: env var
API_KEY = os.environ.get('API_KEY')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
s3 = boto3.resource('s3')


def data_fetcher(event, context):
    stations_req = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations',
        params={
            'apiKey': API_KEY,
            'contract': 'dublin'
        }
    )
    stations = stations_req.json()
    now = datetime.now(tz=timezone.utc)
    key_name = f'{now.year}/{now.month}/{now.day}/{now.isoformat()}.json'

    s3.Bucket(BUCKET_NAME).put_object(Key=key_name, Body=json.dumps(stations))

    return True


if __name__ == "__main__":
    print(data_fetcher("", ""))
