import json
import sqlite3
import facebook
import twitter
import mood
# Check from facebook first, if all goes through fine, then return complete mood result
# Else returns at different levels
# Build caching and updating with sqlite based on the user space the queried person in this layer

# Based on responses from the individual searches, do the textual analysis in this layer
# Update mood analysis for queried person in the user space
# Based on the mood analysis and get mood swings and update queried person in the user space
def search(query):
	result = facebook.searchForUser(query)
	if result["numMatches"] == 0:
		result["actions"]=["DoAgain"]
	elif result["numMatches"] > 1:
		result["actions"]=["Choose"]
	else:
		result = continueFromFacebook(query=query, facebookID=result["matches"][0]["uid"], name=result["matches"][0]["name"])
	return result
def twitterSearch(query):
	return twitter.search(query)

def continueFromFacebook(query, facebookID, name):
	statuses = facebook.recentStatus(facebookID, query)
	streams = facebook.recentStream(facebookID, query)
	#locations = facebook.recentLocationPost(facebookID, query)
	#photos = facebook.recentPhotos(facebookID, query)
	#fbResults = {"statuses": statuses, "streams": streams, "locations": locations, "photos": photos}
	fbResults = {"statuses": statuses, "streams": streams}
	result = twitter.search(name)
	if result["numMatches"] == 0:
		result["actions"]=["DoAgain"]
	elif result["numMatches"] > 1:
		result["actions"]=["Choose"]
	else:
		result = continueFromTwitter(query, fbResults, result["matches"][0]["id"], result["matches"][0]["name"])
	return result

def continueFromTwitter(query, fbResults, twitterID, name):
	twitterResults = twitter.recentTweets(twitterID, query)
	#for r in fbResults:
		#analyzeFb(fbResults[r])
	analyzeFb(fbResults["statuses"])
	analyzeTweets(twitterResults)
	overallResult = overallAnalyze(fbResults, twitterResults)
	continueWithSuggestions(query, overallResult, fbResults["statuses"]["id"], twitterID, name)
	return overallResult

def analyzeTweets(obj):
	for t in obj["results"]:
		t["analysis"] = mood.processTweet(t)
	return obj
def analyzeFb(obj):
	for t in obj["results"]:
		t["analysis"] = mood.processStatus(t)
	return obj
def overallAnalyze(fbObjs, twitterObjs):
	result = {
		"overallMood": "",
		"majorMoods": "",
		"moodsOverTime": [],
		"facebook": fbObjs,
		"twitter": twitterObjs
	}
	return result
def continueWithSuggestions(query, result, facebookID, twitterID, name):
	result["suggestions"] = []
	result["actions"] = []
	return result