from concurrent.futures import ThreadPoolExecutor

import boto3
import json
from . import configure
from django.views.decorators.csrf import csrf_exempt
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features

sqs=boto3.client('sqs', region_name='us-east-1',aws_access_key_id='AKIAJ4D3RPEHAC6CJ3QA',aws_secret_access_key='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')
sns=boto3.client('sns',region_name='us-east-1',aws_access_key_id='AKIAJ4D3RPEHAC6CJ3QA',aws_secret_access_key='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')

@csrf_exempt
def sentimentAnalysis(sqs):
    tweets = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/155818353707/tweetTrend',MessageAttributeNames = ["All"],MaxNumberOfMessages=10)
    for tweet in tweets["Messages"]:
        print(tweet)
        if tweet is not None:
            print(tweet)
            natural_language_understanding = NaturalLanguageUnderstandingV1(
              version='2017-02-27',
              username='19a18919-4bad-4322-b10a-ba08ca5e0bc0',
              password='1JeU7sTAqObg')

            response=natural_language_understanding.analyze(
                text=tweet["Body"],
                features=[features.Sentiment()]
            )
            sTweet={}
            if(response['sentiment']['document']["label"] is not None):

                lan=tweet['MessageAttributes']['lan']

                lon=tweet['MessageAttributes']['lon']
                name=tweet['MessageAttributes']['username']
                time=tweet['MessageAttributes']['timestamp']
                content=tweet['Body']
                sentiment=response['sentiment']['document']["label"]

                sTweet={"location": {"lat": lan, "lon": lon},
                 "username": name,
                 "timestamp": time,
                 "text": content,
                 "sent":sentiment}

           # print(json.dumps(sTweet))
            print(sns.publish(TopicArn=configure.sns_arn,Message=json.dumps(sTweet)))

if __name__ == '__main__':
     thread_pool=ThreadPoolExecutor(max_workers=10)
     while True:
         thread_pool.submit(sentimentAnalysis,sqs)