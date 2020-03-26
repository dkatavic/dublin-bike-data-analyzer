import boto3
import requests
import os
import json
from elasticsearch import Elasticsearch, helpers

ES_HOSTNAME = os.environ.get('ES_HOSTNAME') or "localhost:9200"
BUCKET_NAME = os.environ.get('BUCKET_NAME') or "dublinbikes-dom"

s3_client = boto3.client('s3')

def bulk_json_data(data, _index):
  """
  make stations list iterable and do some mapping of the data (move this later on)
  """
  for doc in data:
    # TODO: refactor this nasty fix, name of coordinate
    doc['position']['lon'] = doc['position']['lng']
    doc['ts'] = doc['last_update']
    del doc['position']['lng']
    yield {
        "_index": _index,
        "_id": f'{doc["contract_name"]}-{doc["number"]}-{doc["last_update"]}',
        "_source": doc
    }

def get_all_keys_in_bucket(s3_client, bucket_name):
  """
  Get all keys in S3 bucket
  """
  print('Fetching objects')
  s3_keys = []
  ContinuationToken = False
  is_done = False
  while not is_done:
    params = {
      'Bucket': bucket_name
    }
    if ContinuationToken:
      params['ContinuationToken'] = ContinuationToken
    s3_response = s3_client.list_objects_v2(**params)
    print(f'MaxKeys: {s3_response["MaxKeys"]}')
    # if hasattr(s3_response, 'NextContinuationToken'):
    if 'NextContinuationToken' in s3_response:
      ContinuationToken = s3_response['NextContinuationToken']
    else:
      is_done = True
      

    for s3object in s3_response['Contents']:
      s3_keys.append(s3object['Key'])
  return s3_keys

s3_object_keys = get_all_keys_in_bucket(s3_client, BUCKET_NAME)
num_of_objects = len(s3_object_keys)
print(f'Total number of S3 objects: {num_of_objects}')

# Fetch S3 Keys and insert into ES
es = Elasticsearch()

for i, key in enumerate(s3_object_keys):
  print(f'Inserting {i+1} of {num_of_objects} object')
  s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
  body_object = s3_object['Body'].read()
  stations = json.loads(body_object)
  response = helpers.bulk(es, bulk_json_data(stations ,"dublin-bikes1"))


print('Finished injecting data')
