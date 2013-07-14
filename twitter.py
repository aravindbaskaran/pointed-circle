# Search for user handle
# If more than one result, send back result
# Based on response, update in user space for that searched query and the number of times the user is chosen
# Fetch recent tweets by user
# Analyze and return similarly

# "https://api.twitter.com/1.1/users/search.json?q=Vineel"
# Authorization:OAuth oauth_consumer_key="DC0sePOBbQ8bYdC8r4Smg",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1373735512",oauth_nonce="-450777365",oauth_version="1.0",oauth_token="326883621-3ee824h2eLDbZC9qTKcaitfkKa9w6EW2adFi6y7X",oauth_signature="iY8tVOqRkShumukRIAQ2iiOr0%2Fo%3D"
# https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=28307354

import requests
import json
import time
import datetime
import utils
from requests_oauthlib import OAuth1
from urlparse import parse_qs
 
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
 
TWITTER_ENDPOINT = "https://api.twitter.com/1.1/$QUERY$"
TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""
TWITTER_OAUTH_TOKEN = ""
TWITTER_OAUTH_TOKENSECRET = ""
TWITTER_OAUTH_HEADER = 'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="$OAUTH_TIME$", oauth_token="$OAUTH_TOKEN$",oauth_version="1.0"'
'''
	{
    "id": 28307354,
    "id_str": "28307354",
    "name": "Vineel Reddy Pindi",
    "screen_name": "vineelreddy",
    "location": "Hyderabd,INDIA.",
    "description": "Mozillian. Community Builder. Mariposa Agency.\r\n\r\nLove People, Cars, Technology, The Web & Pets.",
    "url": "http://t.co/34mHU6UwTT",
    "entities":  {
      "url":  {
        "urls":  [
           {
            "url": "http://t.co/34mHU6UwTT",
            "expanded_url": "http://mariposaagency.com",
            "display_url": "mariposaagency.com",
            "indices":  [
              0,
              22
            ]
          }
        ]
      },
      "description":  {
        "urls":  []
      }
    },
    "protected": false,
    "followers_count": 480,
    "friends_count": 534,
    "listed_count": 19,
    "created_at": "Thu Apr 02 09:05:32 +0000 2009",
    "favourites_count": 186,
    "utc_offset": -28800,
    "time_zone": "Pacific Time (US & Canada)",
    "geo_enabled": true,
    "verified": false,
    "statuses_count": 1867,
    "lang": "en",
    "status":  {
      "created_at": "Sat Jul 13 15:48:15 +0000 2013",
      "id": 356077621030817800,
      "id_str": "356077621030817794",
      "text": "What a day! RT @ydn: All pictures from Day 1 Hack India: Hyderabad can be found here:  http://t.co/QdY1Hc2HzZ #yahoohack",
      "source": "<a href="http://www.tweetdeck.com" rel="nofollow">TweetDeck</a>",
      "truncated": false,
      "in_reply_to_status_id": null,
      "in_reply_to_status_id_str": null,
      "in_reply_to_user_id": null,
      "in_reply_to_user_id_str": null,
      "in_reply_to_screen_name": null,
      "geo": null,
      "coordinates": null,
      "place": null,
      "contributors": null,
      "retweet_count": 2,
      "favorite_count": 0,
      "entities":  {
        "hashtags":  [
           {
            "text": "yahoohack",
            "indices":  [
              110,
              120
            ]
          }
        ],
        "symbols":  [],
        "urls":  [
           {
            "url": "http://t.co/QdY1Hc2HzZ",
            "expanded_url": "http://bit.ly/yflickrindia",
            "display_url": "bit.ly/yflickrindia",
            "indices":  [
              87,
              109
            ]
          }
        ],
        "user_mentions":  [
           {
            "screen_name": "ydn",
            "name": "Y! Developer Network",
            "id": 12904842,
            "id_str": "12904842",
            "indices":  [
              15,
              19
            ]
          }
        ]
      },
      "favorited": false,
      "retweeted": false,
      "possibly_sensitive": false,
      "lang": "en"
    },
    "contributors_enabled": false,
    "is_translator": false,
    "profile_background_color": "EDECE9",
    "profile_background_image_url": "http://a0.twimg.com/profile_background_images/155012792/trumpets.jpg",
    "profile_background_image_url_https": "https://si0.twimg.com/profile_background_images/155012792/trumpets.jpg",
    "profile_background_tile": false,
    "profile_image_url": "http://a0.twimg.com/profile_images/3763348131/1832bda681f47ddfe393c4f0c7802528_normal.jpeg",
    "profile_image_url_https": "https://si0.twimg.com/profile_images/3763348131/1832bda681f47ddfe393c4f0c7802528_normal.jpeg",
    "profile_banner_url": "https://pbs.twimg.com/profile_banners/28307354/1370532547",
    "profile_link_color": "088253",
    "profile_sidebar_border_color": "D3D2CF",
    "profile_sidebar_fill_color": "E3E2DE",
    "profile_text_color": "634047",
    "profile_use_background_image": false,
    "default_profile": false,
    "default_profile_image": false,
    "following": true,
    "follow_request_sent": false,
    "notifications": false
  }
'''
def search(name):
	query = "/users/search.json?q="+name
	response = fireRequest(query)
	numResults = len(response)
	result = {"type": "Twitter", "qtype": "search", "query": query, "numMatches": numResults,"matches": []}
	for match in response:
		result["matches"].append(match)
	return result

def recentTweets(twitterID, query):
	query = "statuses/user_timeline.json?user_id="+str(twitterID)+"&count=20"
	response = fireRequest(query)
	numResults = len(response)
	result = utils.result("Twitter", id=twitterID, qtype="status", query=query, numResults=numResults)
	for match in response:
		result["results"].append(match)
	return result

def fireRequest(query):
	oauth = OAuth1(TWITTER_CONSUMER_KEY,
                   client_secret=TWITTER_CONSUMER_SECRET,
                   resource_owner_key=TWITTER_OAUTH_TOKEN,
                   resource_owner_secret=TWITTER_OAUTH_TOKENSECRET)
	url = TWITTER_ENDPOINT.replace("$ACCESS_TOKEN$", TWITTER_OAUTH_TOKEN).replace("$QUERY$", query)
	#t = str(int(time.time()))
	#headers = {'Authorization': TWITTER_OAUTH_HEADER.replace("$ACCESS_TOKEN$", TWITTER_OAUTH_HEADER).replace("$OAUTH_TIME$", t)}
	utils.logger.debug("Twitter - " + url)
	r = requests.get(url=url, auth=oauth)
	#utils.logger.debug("Twitter - " + r.text)
	return r.json()