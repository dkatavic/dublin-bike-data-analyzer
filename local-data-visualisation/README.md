# local-data-visualisation

This folder consist of local EL(K) stack and a script that fetches data from S3 and injects it into ES

Structure:
* docker-compose.yml 
* es_templates.json - templates, may need to do transform to support ES native geo_point

## How to run

### Spin up EK

from this directory run

```
docker-compose up
```

inject ES templates by logging into kibana http://localhost:5601 -> Dev Tools and execute content of ./es-templates.json file

```
PUT _template/template
{
  "index_patterns": ["dublin-bikes*"],
  "order": 10,
  "version": 1,
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "number": {
        "type": "integer"
      },
      "contract_name": {
        "type": "keyword"
      },
      "name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "address": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "position": {
        "type": "geo_point"
      },
      "banking": {
        "type": "boolean"
      },
      "bonus": {
        "type": "boolean"
      },
      "bike_stands": {
        "type": "integer"
      },
      "available_bike_stands": {
        "type": "integer"
      },
      "available_bikes": {
        "type": "integer"
      },
      "status": {
        "type": "keyword"
      },
      "last_update": {
        "type": "date"
      },
      "ts": {
        "type": "date"
      }
    }
  }
}
```

### Inject data from S3

`inject_data.py` will fetch all data in S3 and inject it into ES. Change configuration variables if needed

Rn
```
pipenv shell
python inject_data.py
```
