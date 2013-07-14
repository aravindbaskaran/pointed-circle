# Single status analysis
# Parse and get tokenize, lemmatize and PoS.
# Compare for presence of specific patterns, special words, smileys and abbreviations
# Return an array of moods

# For a collection of mood arrays based on time, find out what is the mood change pattern
# For eg: 5 days back happy, 2 days back satisfied, today tired
# Get a mood swing visualization for this
import json
import nltk
import re
from pprint import pprint
from sets import Set
import utils
import requests
from senti_classifier import senti_classifier

_moodfiles = [
	"anger", "joy", "sad", "sarcasm"
];
_regexes = [
	["(?i)(a+rgh|angry|annoyed|annoying|appalled|bitter|cranky|hate|hating|mad)","(?i)(wtf|wth|omfg|hell|ass|bitch|bullshit|bloody|fucking?|shit+y?|crap+y?)\b|\b(fuck|damn|piss|screw|suck)e?d?"],
	["(?i)(ha(ha)+|he(he)+|lol|rofl|lmfao|lulz|lolz|rotfl|lawl|hilarious)","(?i)(fantastic|what a day|yes|yay|hallelujah|hurray|bingo|amused|cheerful|excited|glad|proud)"],
	["(?i)(what the hell|oh shit|yikes|gosh|baffled|stumped|surprised|shocked)"],
	["(?i)(meh|yikes|gosh|baffled|stumped|surprised|shocked|forget it|get lost|whatever)"]
]
_intensifiers = [
	"Absolutely","Achoo","Ack","Ahh","Aha","Ahem","Ahoy","Agreed","Alas","Alright","Alrighty","Alrighty-roo","Alack",
	"Amen","Anytime","Argh","Anyhoo","Anyhow","As if","Attaboy","Attagirl","Awww","Awful","Bam","Bah humbug","Behold",
	"Bingo","Blah","Bless you","Boo","Bravo","Cheers","Crud","Darn","Dang","Doh","Drat","Duh","Eek","Eh","Gee","Geepers",
	"Gee Whiz","Golly","Goodnes","Goodness Gracious","Gosh","Ha","Hallelujah","Hey","Hi","Hmm","Huh","Indeed","Jeez",
	"My gosh","No","Now","Nah","Oops","Ouch","Phew","Please","Rats","Shoot","Shucks","There","Tut","Uggh","Waa","What",
	"Woah","Woops","Wow","Yay","Yes","Yikes"
]
'''
	{
		"words": [], // Verbs and adjectives only for PoS verification
		"smileys": [], // Check with whole statement
		"phrases": [], // Check with whole statement
		"abbreviations": [], // Check with tokens
		"regexes": []
	}
'''
_moodMetas = []
def init():
	for index, m in enumerate(_moodfiles):
		json_data=open('./Flask/mood_base/'+m+'.json')
		data = json.load(json_data)
		pprint(data)
		data["r"] = []
		for reg in _regexes[index]:
			data["r"].append(re.compile(reg))
		json_data.close()
		_moodMetas.append(data)
	#utils.logger.debug("Files loaded")

def processTweet(tweet):
	posneg = sentimentalize(tweet["text"])
	__moo = mood(tweet["text"])
	# Check for media, location, retweet, people
	intensity = len(tweet["entities"]["user_mentions"])  + len(tweet["entities"]["hashtags"]) + len(tweet["entities"]["urls"]) + (len(tweet["entities"]["media"]) if "media" in tweet["entities"] else 0) + tweet["retweet_count"]
	result = {"positive": posneg[0], "negative": posneg[1], "intensity": intensity,"moods": __moo[0], "time": tweet["created_at"], "moodWords": __moo[1]}
	return result
def processStatus(status):
	msg = status["message"] #+ ". " + (status["description"] if "description" in status & status["description"] != None else "")
	posneg = sentimentalize(msg)
	__moo = mood(msg)
	intensity = status["likes"]["count"] + (len(status["comments"]["data"]) if "comments" in status else 0)
	result = {"positive": posneg[0], "negative": posneg[1], "intensity": intensity,"moods": __moo[0], "time": status["created_time"], "moodWords": __moo[1]}
	return result
def tokenize(s):
	return nltk.word_tokenize(s)
def possize(tokens):
	return nltk.pos_tag(tokens)
def mood(s):
	moods = []
	mood_words = Set()
	for _mood in _moodMetas:
		mood = 0
		mood_Words = []
		wordlist = nltk.FreqDist(tokenize(s))
		word_features = Set(wordlist.keys())
		mood_words = mood_words | (word_features & Set(_mood["words"]))
		mood = mood + len(mood_words)
		for regex in _mood["r"]:
			mood = mood + len(regex.findall(s))
		for smiley in _mood["smileys"]:
			mood = mood + str.count(s, str(smiley))
		for phrase in _mood["phrases"]:
			ms = str.count(s.lower(), phrase.lower())
			mood = mood + ms
			if ms > 0:
				mood_words.add(phrase)
		moods.append(mood)
	return [moods,list(mood_words)]

def sentimentalize(s):
	pos_score, neg_score = senti_classifier.polarity_scores([s])
	return [pos_score, neg_score]
init()
#print mood("What a day!")