from elasticsearch import Elasticsearch
from datetime import datetime
from datetime import date
import json

ELK_SERVER="http://10.1.93.208:9200"
XDATA_INDEX="xdata"

def searchElasticSearch(queryData):
	matches = es.search(index="xdata", body=queryData)
	if len(matches['hits']['hits']) == 0:
		print "No Hits found for search."
	else:
		print "Search Run return %d match with max score of %f" % \
			  (matches['hits']['total'], matches['hits']['max_score'])

# String Query format found in 
# http://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax
def searchElasticSearchLucene(queryData):
	matches = es.search(index="xdata", q=queryData)
	if len(matches['hits']['hits']) == 0:
		print "No Hits found for search."
	else:
		print "Search Run return %d match with max score of %f" % \
			  (matches['hits']['total'], matches['hits']['max_score'])
	return matches


es = Elasticsearch(ELK_SERVER)

# Query All the Logs
queryData='{ "query": { "match_all": {}} }'
searchElasticSearch(queryData)

# Query Logs that have the activity select
queryData = 'parms.activity:"select"'
searchElasticSearchLucene(queryData)

# Query logs that have the activity select | alter
queryData = 'parms.activity:("select" OR "alter")'
searchElasticSearchLucene(queryData)


def printResults(results):
	for h in results['hits']:
		print h

queryData = {}
jsonQueryData = json.dumps(queryData)
fieldFilter = ["timestamp", "sessionID"]

print "==============================================="
queryData["query"] = {"match_all": {}}
results = es.search(index="xdata", body=jsonQueryData, fields=fieldFilter)['hits']
printResults(results)

print "==============================================="
results = es.search(index="xdata", body=jsonQueryData, fields=fieldFilter, sort="timestamp:asc")['hits']
printResults(results)

print "==============================================="
results = es.search(index="xdata", body=jsonQueryData, fields=fieldFilter, sort="timestamp:desc", size=1)['hits']
printResults(results)

# ElasticSearch-py API
# http://elasticsearch-py.readthedocs.org/en/latest/api.html#elasticsearch

# Aggregation Types
# http://www.elastic.co/guide/en/elasticsearch/reference/1.x/search-aggregations.html

# Filter Types 
# http://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-filters.html

print "==============================================="
print "Number of Sessions Stored in Elastic Search"
queryData["aggs"] = {}
queryData["aggs"]["num_sessions"] = { "cardinality" : { "field": "sessionID" } };
jsonQueryData = json.dumps(queryData)
results = es.search(index="xdata", body=jsonQueryData, fields=fieldFilter)
print results['aggregations']

print "==============================================="
print "Number of Sessions Per Day"
queryData["aggs"]["num_sessions_per_day"] = {
	"date_histogram": {
		"field": "timestamp",
		"interval": "day"
	},
	"aggs": { 
		"count": { 
			"cardinality" : { "field": "sessionID" }
		},
	}
}
jsonQueryData = json.dumps(queryData)
results = es.search(index="xdata", body=jsonQueryData)
print results['aggregations']


print "==============================================="
print "Number of Sessions Last 12hrs"
queryData["aggs"]["12hours"] = {
	"filter": { 
		"range": {
			"timestamp": {
				"lte": "now",
				"gt": "now-12h"
			}
		}
	},
	"aggs": {
		"sessionCount": {
			"cardinality": { "field": "sessionID" },
		}
	}
}
jsonQueryData = json.dumps(queryData)
results = es.search(index="xdata", body=jsonQueryData, fields=fieldFilter)
print results['aggregations']

print "================================================="
print "Activity Codes for Each Session in the last 12 Hours"
queryData["aggs"]["12hours"]["aggs"] = { 
	"sessions": { 
		"terms": { "field": "sessionID" },
		"aggs": {
			"activities": {
				"terms": { "field": "parms.activity" }
			}
		}
	}
}
jsonQueryData = json.dumps(queryData)
results = es.search(index="xdata", body=jsonQueryData, fields=fieldFilter)
for session in  results['aggregations']["12hours"]["sessions"]["buckets"]:
	print session
