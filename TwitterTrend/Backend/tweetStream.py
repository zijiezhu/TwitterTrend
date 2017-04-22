from tweepy import OAuthHandler
import time
from tweepy import Stream
from tweepy import OAuthHandler
from TwitterTrend.Backend.tweetListener import tweetListener
from . import configure

if __name__ == '__main__':
    __customerKey = configure.customerKey
    __customerSecret = configure.customerSecret
    __accessToken = configure.accessToken
    __accessSecret = configure.accessSecret
    autho = OAuthHandler(__customerKey, __customerSecret)
    autho.set_access_token(__accessToken, __accessSecret)
    url = "https://stream.twitter.com/1.1/statuses/sample.json"
    stream = Stream(autho, tweetListener())
    while True:
       try:
        stream.filter(locations=[-180,-90,180,90],stall_warnings = True)
       except:
         continue


