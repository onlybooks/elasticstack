from elasticsearch import Elasticsearch

es = Elasticsearch()

doc = {"name": "kim", "age": 35}
res = es.index(index='test_index', body=doc)
print(res)

doc = {
        "size": 1,
        "query": {
          "term": {
            "DestCityName": "Seoul"
          }
        }
      }

res = es.search(index='kibana_sample_data_flights', body=doc)
print(res)
