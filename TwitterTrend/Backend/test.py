from elasticsearch import Elasticsearch

# domain="search-tweetmap-tx3gypzkmdsydrnlqv44ojd5qq.us-east-1.es.amazonaws.com"
# es=Elasticsearch(hosts= [{'host':domain, 'port': 80,'use_ssl': False}])
# body = {"mappings": {"tweet": {
#         "properties": {"username": {"type": "string"}, "timestamp": {"type": "date"}, "location": {"type": "geo_point"},
#                        "text": {"type": "string"},"sent":{"type":"string"}}}}}
# print(es.indices.create(index='tweettrend',ignore=400,body=body))body
from TwitterTrend.Backend.application import storeToES

message="{\"text\": \"@Natures_Voice hello we saw this today over Penzance, is it a buzzard? https://t.co/8OqoFFOin2\", \"sent\": \"positive\", \"lat\": {\"DataType\": \"String\", \"StringValue\": \"49.882472\"}, \"username\": {\"DataType\": \"String\", \"StringValue\": \"Budgies Roadtrip\"}, \"lon\": {\"DataType\": \"String\", \"StringValue\": \"-6.368504\"}, \"timestamp\": {\"DataType\": \"String\", \"StringValue\": \"1492716914082\"}}"
storeToES(message)

