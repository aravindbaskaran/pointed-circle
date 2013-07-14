import json
def result(type, id, qtype, query, numResults):
	return {"type": type, "id": id, "qtype": qtype, "query": query, "numResults": numResults,"results": [], "actions": [],
	"suggestions": [], "moods": []}	