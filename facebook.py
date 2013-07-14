# TODO Check for expiry and update token
import requests
import json
import time
import datetime
import utils

# !!! Delete before commit !!!
FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
FACEBOOK_ACCESS_TOKEN = ""
FACEBOOK_FQL_ENDPOINT = "https://graph.facebook.com/fql?q=$QUERY$&format=json&access_token=$ACCESS_TOKEN$"
FACEBOOK_GRAPH_ENDPOINT = "https://graph.facebook.com/$QUERY$format=json&access_token=$ACCESS_TOKEN$"
# Optionally set default permissions to request, e.g: ['email', 'user_about_me']
FACEBOOK_SCOPE = ["email","read_friendlists","read_insights","read_mailbox","read_requests","read_stream","user_online_presence","friends_online_presence"
	"user_about_me", "user_activities","user_birthday","user_checkins","user_education_history","user_events","user_groups","user_hometown","user_interests",
	"user_likes", "user_location", "user_notes", "user_photos", "user_questions", "user_relationships", "user_relationship_details", "user_religion_politics", "user_status"
	"user_subscriptions", "user_videos", "user_website", "user_work_history", "friends_work_history", "friends_website", "friends_videos", "friends_subscriptions",
	"friends_status", "friends_religion_politics", "friends_relationship_details", "friends_relationships", "friends_questions", "friends_photos", "friends_notes",
	"friends_location", "friends_likes", "friends_interests", "friends_hometown", "friends_groups", "friends_events", "friends_education_history", "friends_checkins",
	"friends_birthday", "friends_activities", "friends_about_me"]
TYPES = ["FQL","GRAPH"]
# https://www.facebook.com/dialog/oauth?response_type=token&display=popup&client_id=145634995501895&redirect_uri=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2Fcallback&scope=email%2Cpublish_actions%2Cuser_about_me%2Cuser_actions.books%2Cuser_actions.music%2Cuser_actions.news%2Cuser_actions.video%2Cuser_activities%2Cuser_birthday%2Cuser_education_history%2Cuser_events%2Cuser_games_activity%2Cuser_groups%2Cuser_hometown%2Cuser_interests%2Cuser_likes%2Cuser_location%2Cuser_notes%2Cuser_photos%2Cuser_questions%2Cuser_relationship_details%2Cuser_relationships%2Cuser_religion_politics%2Cuser_status%2Cuser_subscriptions%2Cuser_videos%2Cuser_website%2Cuser_work_history%2Cfriends_about_me%2Cfriends_actions.books%2Cfriends_actions.music%2Cfriends_actions.news%2Cfriends_actions.video%2Cfriends_activities%2Cfriends_birthday%2Cfriends_education_history%2Cfriends_events%2Cfriends_games_activity%2Cfriends_groups%2Cfriends_hometown%2Cfriends_interests%2Cfriends_likes%2Cfriends_location%2Cfriends_notes%2Cfriends_photos%2Cfriends_questions%2Cfriends_relationship_details%2Cfriends_relationships%2Cfriends_religion_politics%2Cfriends_status%2Cfriends_subscriptions%2Cfriends_videos%2Cfriends_website%2Cfriends_work_history%2Cfriends_online_presence%2Cread_friendlists%2Cread_insights%2Cread_mailbox%2Cread_page_mailboxes%2Cread_requests%2Cread_stream%2Cuser_online_presence


# Search for user
# Check with the user if you are choosing the right person for multiple search results
# Based on response, update in user space for that searched query and the number of times the user is chosen
# Now fetch recent 1. status, 2. stream, 3. location_post, 4. photo
# If no recent posts, return "Nowhere to be found", update in user space for the person, ask if needs to be searched further
# else recent posts are found, analyze based on type for information
# If nothing is available < 5 days from today, send back with suggestion to try calling them

SEARCH_QUERY = "SELECT uid, name, sex, about_me, age_range, pic_cover, online_presence, pic_with_logo from user where uid in (SELECT uid2 FROM friend WHERE uid1 = me()) and (strpos(lower(name),'$QUERY$')>=0 OR strpos(name,'$QUERY$')>=0)"
'''
	{
  "data": [
    {
      "uid": 123129, 
      "name": "Name", 
      "sex": "male", 
      "about_me": null, 
      "age_range": null, 
      "pic_cover": {
        "cover_id": "12312", 
        "source": "https://fbcdn-sphotos-f-a.akamaihd.net/hphotos-ak-ash4/s720x720/215771_10151122916046116_1472431541_n.jpg", 
        "offset_y": 54, 
        "offset_x": 0
      }, 
      "online_presence": "offline", 
      "pic_with_logo": "https://fbexternal-a.akamaihd.net/safe_image.php?d=AQCLu8ajS04qyu3T&url=https%3A%2F%2Ffbcdn-profile-a.akamaihd.net%2Fhprofile-ak-prn1%2F174525_522066115_772494068_s.jpg&logo&v=5"
    }
  ]
}
'''
def searchForUser(query):
	fql = SEARCH_QUERY.replace("$QUERY$", query)
	response = fireRequest(fql, TYPES[0])
	numResults = len(response["data"])
	utils.logger.debug("FB - Search by user matches - " + str(numResults))
	result = {"type": "Facebook", "qtype": "search", "query": query, "numMatches": numResults,"matches": []}
	for match in response["data"]:
		result["matches"].append(match)
	return result

#522066115/posts?limit=10&since=1373653899
STATUS_QUERY = "$UID$/posts?limit=10&since=$TIME$&"
#"SELECT source,message,comment_info,like_info,uid from status where uid=$UID$ limit 10"
'''
	{
  "data": [
    {
"id": "522066115_10151421968376116",
"from": {
"name": "Vineel Reddy Pindi",
"id": "522066115"
},
"message": "",
"picture": "",
"link": "http://t.co/QdY1Hc2HzZ",
"name": "Hack India: Hyderabad 2013",
"caption": "bit.ly",
"description": "Sets let you organize your photos on Flickr. Explore the 407 photos in this set.",
"icon": "https://fbcdn-photos-c-a.akamaihd.net/hphotos-ak-prn1/851565_10151397911967544_632525583_n.png",
"type": "link",
"status_type": "app_created_story",
"application": {
"name": "Twitter",
"namespace": "twitter",
"id": "2231777543"
},
"created_time": "2013-07-13T15:48:19+0000",
"updated_time": "2013-07-13T15:48:19+0000",
"count": 5
}
}
	]
}
'''
DIFFTIME = 15 * 86400
def recentStatus(userID, query):
	fql = STATUS_QUERY.replace("$UID$", str(userID)).replace("$TIME$", str(int(time.time()) - DIFFTIME))
	response = fireRequest(fql, TYPES[1])
	numResults = len(response["data"])
	result = utils.result("Facebook", id=userID, qtype="status", query=query, numResults=numResults)
	for match in response["data"]:
		result["results"].append(match)
	return result

STREAM_QUERY = "SELECT type,description,message, share_count , with_tags, comment_info, updated_time, like_info, source_id from stream where source_id = $UID$ and updated_time > $TIME$"
'''
	{
      "type": 237, 
      "description": null, 
      "message": "What a day! RT @ydn: All pictures from Day 1 Hack India: Hyderabad can be found here:  http://t.co/QdY1Hc2HzZ #yahoohack", 
      "share_count": 0, 
      "with_tags": [
      ], 
      "comment_info": {
        "can_comment": true, 
        "comment_count": 0, 
        "comment_order": "chronological"
      }, 
      "updated_time": 1373730499, 
      "like_info": {
        "can_like": true, 
        "like_count": 5, 
        "user_likes": false
      }, 
      "source_id": 522066115
    }
'''
def recentStream(userID, query):
	fql = STREAM_QUERY.replace("$UID$", str(userID)).replace("$TIME$", str(int(time.time()) - DIFFTIME))
	response = fireRequest(fql, TYPES[0])
	numResults = len(response["data"])
	result = utils.result("Facebook", id=userID, qtype="stream", query=query, numResults=numResults)
	for r in response["data"]:
		result["results"].append(r)
	return result

LOCATION_POST_QUERY = "SELECT coords,message, author_uid, timestamp from location_post where author_uid = $UID$ and timestamp > $TIME$"
def recentLocationPost(userID, query):
	fql = LOCATION_POST_QUERY.replace("$UID$", str(userID)).replace("$TIME$", str(int(time.time()) - DIFFTIME))
	response = fireRequest(fql, TYPES[0])
	numResults = len(response["data"])
	result = utils.result("Facebook", id=userID, qtype="location_post", query=query, numResults=numResults)
	for r in response["data"]:
		result["results"].append(r)
	return result
	
PHOTO_QUERY = "select owner, src, modified from photo where owner = 522066115 and modified > $TIME$"
def recentPhotos(userID, query):
	fql = PHOTO_QUERY.replace("$UID$", str(userID)).replace("$TIME$", str(int(time.time()) - DIFFTIME))
	response = fireRequest(fql, TYPES[0])
	numResults = len(response["data"])
	result = utils.result("Facebook", id=userID, qtype="photo", query=query, numResults=numResults)
	for r in response["data"]:
		result["results"].append(r)
	return result

def fireRequest(q, type):
	url = (FACEBOOK_FQL_ENDPOINT if type == TYPES[0] else FACEBOOK_GRAPH_ENDPOINT).replace("$ACCESS_TOKEN$", FACEBOOK_ACCESS_TOKEN).replace("$QUERY$", q)
	utils.logger.debug("FB - " + url)
	r = requests.get(url)
	#utils.logger.debug("FB - Response received - " + r.text)
	return r.json()

def getLikesAndInterests(userID):
	return

# Recommend things user to ask them to suggest the friend to do things that he/she has liked, added in recent times, books, movies, music,etc.
# Check graph API for this information