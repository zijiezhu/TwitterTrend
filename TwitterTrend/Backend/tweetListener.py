from tweepy.streaming import StreamListener
import json
import boto3
from . import configure
maxTweets = 100

class tweetListener(StreamListener):

    print('here')

    def __init__(self):
        self.sqs= boto3.client('sqs', region_name='us-east-1',aws_access_key_id= configure.aws_access_key_id,aws_secret_access_key= configure.aws_secret_access_key)
        self.index=0

    def on_data(self, __rawData):
        print('here0')
        if __rawData:
            __count = 0
            jsonData = json.loads(__rawData)
            if jsonData.get("user") is not None and jsonData.get("user").get("name"):
                name = jsonData.get("user").get("name")
                __count = __count + 1
                print('here1')
            if jsonData.get("coordinates"):
                geo = jsonData.get("coordinates").get("coordinates")
                long = geo[0]
                lan = geo[1]
                __count = __count + 1
                print('here2')
            elif jsonData.get("place"):
                geo = jsonData.get("place").get("bounding_box").get("coordinates")[0]
                long = geo[0][0]
                lan = geo[0][1]
                __count = __count + 1
                print('here3')
            if jsonData.get("text"):
                content = jsonData.get("text")
                __count = __count + 1

            if jsonData.get("timestamp_ms"):
                time = jsonData.get("timestamp_ms")
                __count = __count + 1
                print('here4')

            if __count == 4 and jsonData.get('lang')=='en' :
                print('here5')
                self.index = self.index % maxTweets + 1
                attributes = {"username":{"StringValue":name,"DataType":"String"},
                              "lan":{"StringValue":str(lan),"DataType":"String"},
                              "lon":{"StringValue":str(lan),"DataType":"String"},
                              "timestamp":{"StringValue":time,"DataType":"String"}
                              }

                self.sqs.send_message(QueueUrl=configure.sqs_arn, MessageBody=content, MessageAttributes=attributes)
                print('here7')

            {"created_at": "Thu Apr 20 19:41:13 +0000 2017", "id": 855144341534371841, "id_str": "855144341534371841",
             "text": "\ud83d\ude04 https:\/\/t.co\/rIuwfNs4IY", "display_text_range": [0, 1],
             "source": "\u003ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003eTwitter for iPhone\u003c\/a\u003e",
             "truncated": false, "in_reply_to_status_id": null, "in_reply_to_status_id_str": null,
             "in_reply_to_user_id": null, "in_reply_to_user_id_str": null, "in_reply_to_screen_name": null,
             "user": {"id": 2360637557, "id_str": "2360637557", "name": "mila", "screen_name": "maykiiix",
                      "location": "adapazar\u0131 ", "url": null, "description": "\u03dc\u03d3\u017f\u03de",
                      "protected": false, "verified": false, "followers_count": 310, "friends_count": 120,
                      "listed_count": 0, "favourites_count": 4324, "statuses_count": 220,
                      "created_at": "Sun Feb 23 11:28:02 +0000 2014", "utc_offset": 10800, "time_zone": "Kyiv",
                      "geo_enabled": true, "lang": "tr", "contributors_enabled": false, "is_translator": false,
                      "profile_background_color": "C0DEED",
                      "profile_background_image_url": "http:\/\/pbs.twimg.com\/profile_background_images\/444119123593670656\/5UcT95_v.jpeg",
                      "profile_background_image_url_https": "https:\/\/pbs.twimg.com\/profile_background_images\/444119123593670656\/5UcT95_v.jpeg",
                      "profile_background_tile": true, "profile_link_color": "0084B4",
                      "profile_sidebar_border_color": "FFFFFF", "profile_sidebar_fill_color": "DDEEF6",
                      "profile_text_color": "333333", "profile_use_background_image": true,
                      "profile_image_url": "http:\/\/pbs.twimg.com\/profile_images\/854332509823406081\/cCclbnUP_normal.jpg",
                      "profile_image_url_https": "https:\/\/pbs.twimg.com\/profile_images\/854332509823406081\/cCclbnUP_normal.jpg",
                      "profile_banner_url": "https:\/\/pbs.twimg.com\/profile_banners\/2360637557\/1491606706",
                      "default_profile": false, "default_profile_image": false, "following": null,
                      "follow_request_sent": null, "notifications": null}, "geo": null, "coordinates": null,
             "place": {"id": "0b5219d6ce6a63ee",
                       "url": "https:\/\/api.twitter.com\/1.1\/geo\/id\/0b5219d6ce6a63ee.json", "place_type": "admin",
                       "name": "Adapazar\u0131", "full_name": "Adapazar\u0131, Sakarya", "country_code": "TR",
                       "country": "T\u00fcrkiye", "bounding_box": {"type": "Polygon", "coordinates": [
                     [[30.228445, 40.734714], [30.228445, 40.963103], [30.594337, 40.963103], [30.594337, 40.734714]]]},
                       "attributes": {}}, "contributors": null, "is_quote_status": false, "retweet_count": 0,
             "favorite_count": 0, "entities": {"hashtags": [], "urls": [], "user_mentions": [], "symbols": [],
                                               "media": [{"id": 855144330088124417, "id_str": "855144330088124417",
                                                          "indices": [2, 25],
                                                          "media_url": "http:\/\/pbs.twimg.com\/media\/C94VPMqXkAEB774.jpg",
                                                          "media_url_https": "https:\/\/pbs.twimg.com\/media\/C94VPMqXkAEB774.jpg",
                                                          "url": "https:\/\/t.co\/rIuwfNs4IY",
                                                          "display_url": "pic.twitter.com\/rIuwfNs4IY",
                                                          "expanded_url": "https:\/\/twitter.com\/maykiiix\/status\/855144341534371841\/photo\/1",
                                                          "type": "photo",
                                                          "sizes": {"medium": {"w": 480, "h": 797, "resize": "fit"},
                                                                    "large": {"w": 480, "h": 797, "resize": "fit"},
                                                                    "thumb": {"w": 150, "h": 150, "resize": "crop"},
                                                                    "small": {"w": 410, "h": 680, "resize": "fit"}}}]},
             "extended_entities": {"media": [
                 {"id": 855144330088124417, "id_str": "855144330088124417", "indices": [2, 25],
                  "media_url": "http:\/\/pbs.twimg.com\/media\/C94VPMqXkAEB774.jpg",
                  "media_url_https": "https:\/\/pbs.twimg.com\/media\/C94VPMqXkAEB774.jpg",
                  "url": "https:\/\/t.co\/rIuwfNs4IY", "display_url": "pic.twitter.com\/rIuwfNs4IY",
                  "expanded_url": "https:\/\/twitter.com\/maykiiix\/status\/855144341534371841\/photo\/1",
                  "type": "photo", "sizes": {"medium": {"w": 480, "h": 797, "resize": "fit"},
                                             "thumb": {"w": 150, "h": 150, "resize": "crop"},
                                             "small": {"w": 410, "h": 680, "resize": "fit"}}}]}, "favorited": false,
             "retweeted": false, "possibly_sensitive": false, "filter_level": "low", "lang": "und",
             "timestamp_ms": "1492717273492"}