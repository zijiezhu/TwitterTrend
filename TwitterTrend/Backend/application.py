import json
import boto3
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
from . import configure
from django.http import request

es=Elasticsearch(hosts=[{'host': configure.es_domain,'port':80,'use_ssl':False}])
index=0
message_queue = []

@csrf_exempt
def snsFunction(request):

    message_queue.append(request)
    try:
        raw_data = json.loads(request.data)

    except:
        print("Unable to load request")
        pass

    headers = request.headers.get('X-Amz-Sns-Message-Type')
    print(raw_data)

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in raw_data:
        url = request.get(raw_data['SubscribeURL'])
        print(url)
    elif headers == 'Notification':
         notification = raw_data["Message"]
         storeToES(notification)

    else:
        print("Headers not specified")

    print("here")
    return "OK\n"
{"Type": "Notification", "MessageId": "798e552d-25f1-506a-97f8-04598ce40d05",
         "TopicArn": "arn:aws:sns:us-east-1:000916848138:twittertrend",
         "Message": "{\"content\": \"@Natures_Voice hello we saw this today over Penzance, is it a buzzard? https://t.co/8OqoFFOin2\", \"sentiment\": \"positive\", \"lat\": {\"DataType\": \"String\", \"StringValue\": \"49.882472\"}, \"username\": {\"DataType\": \"String\", \"StringValue\": \"Budgies Roadtrip\"}, \"long\": {\"DataType\": \"String\", \"StringValue\": \"-6.368504\"}, \"timestamp_ms\": {\"DataType\": \"String\", \"StringValue\": \"1492716914082\"}}",
         "Timestamp": "2017-04-22T00:41:57.094Z", "SignatureVersion": "1",
         "Signature": "RyJfUIZ9eDdXGR6j9L0o/Lw9Dph607sqX8Slw1YmwnmqLO8eAc143j8uV7ft82T8r12mtE+LfG8s1bpbnNp6yOz/ZgYgfBBv+gY6n4AT9OCX4gOR0Gu+XnSyErG/CoExDmI2+FxrQN5xIuq9VSNu/+NhptwHGt15uKV40Hu6Zm3HMQbiAfll1x5JQrhkyhomQ6xqz31kN0yhthmvsRjk34aOiNvKm8+37zGM5IMvmGRjMR4l397oFIqvLExOt/Lt12yBQRzct5EsznHytVic7j6TENnPJpUxyIskt/M47udqA3PlOa9JzbT+kRbkbPFKmHxgrMn24qdAt9k4yIN+nQ==",
         "SigningCertURL": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-b95095beb82e8f6a046b3aafc7f4149a.pem",
         "UnsubscribeURL": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:000916848138:twittertrend:7bf21d9c-9117-4fbd-bf88-170a876480e1"}

def storeToES(notification):
    raw_data=json.loads(notification)

    name=raw_data["username"]["StringValue"]
    long=raw_data["lon"]["StringValue"]
    lan=raw_data["lat"]["StringValue"]
    content=raw_data["text"]
    timestamp=raw_data["timestamp"]["StringValue"]
    sentiment=raw_data["sent"]

    data={"username":name,"timestamp":timestamp,"location":{"lat":lan,"lon":long},"text":content,"sent":sentiment}
    es.index(index="tweettrend", doc_type='tweet', id=index, body=json.dumps(data))

def get_geo(lat, long):
    data = es.search(index="tweetTrend", body={"query": {"bool": {"must": {"match_all": {}}, "filter": {
        "geo_distance": {"distance": "200km", "location": {"lat": lat, "lon": long}}}}}})['hits']
    try:
        response = HttpResponse(json.dumps(data), content_type="application/json")
        return response
    except:
        print("error")

def get_query(keyword):
    keyword = re.sub('[^A-Za-z0-9]+', '', keyword)
    data = es.search(index="tweetTrend",
                     body={"sort": [{"timestamp": {"order": "desc"}}], "query": {"match": {"text": keyword}},
                           "size": 100})['hits']
    response = HttpResponse(json.dumps(data), content_type="application/json")
    return response


def update():
    if message_queue:
        return HttpResponse(message_queue.pop(-1))
    else:
        return HttpResponse("hello")





