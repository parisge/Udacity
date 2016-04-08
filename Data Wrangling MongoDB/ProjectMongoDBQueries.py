# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 13:03:10 2015

@author: GEP
"""
from pymongo import MongoClient
import pprint


client = MongoClient("mongodb://localhost:27017")
db = client.openstreetdata


def userContributions():
    pipeline = [
                {'$match': {"created.user":{'$exists':1}}},
                {"$group": { "_id" : "$created.user",  "count" : {"$sum" : 1 }}},
                {"$sort": {"count" : -1}},
                {"$limit" : 10}
    
    ]    
    result = db.map.aggregate(pipeline)
    
    return result
 
def countAddresses():
    return db.map.count( {"address" : {"$exists" : 1}}  )
    
def addressGroupByCitySuburb():
    pipeline = [
        {"$match":  {"address" : {"$exists" : 1}}},   
        {"$group": {"_id": {"city": "$address.city", "suburb" : "$address.suburb" }, "count" : {"$sum" : 1}}},
        {"$sort": {"count" : -1}},
        {"$limit" : 5}
    ]
    result = db.map.aggregate(pipeline)
    
    return result

#input: field = field name in address subdocument 
def count_incomplete_addresses(field):
    pipeline = [
        {"$match":  {"address" : {"$exists" : 1}, "address." + field : {"$exists" : 0}}},        
        {"$group": {"_id": "Addresses", "count" : {"$sum" : 1}}},
    ]
    result = db.map.aggregate(pipeline)
    
    return result

def uniqueusers():
    pipeline = [
        {"$group": {"_id": "$created.user"}},
        {"$group": {"_id":1, "count":{"$sum":1}}}
    ]
    result =db.map.aggregate(pipeline)
    return result
    
def singlepostusers():
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, 
                {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, 
                {"$sort":{"_id":1}}, {"$limit":1}]
    result =db.map.aggregate(pipeline)
    return result            

print "Number of documents"
print db.map.find().count()
print "============================================================"

print "Number of nodes"
print db.map.find({"type":"node"}).count()
print "============================================================"

print "Number of ways"
print db.map.find({"type":"way"}).count()
print "============================================================"

print "Number of unique users"
pprint.pprint(list(uniqueusers()))
print "============================================================"

print "Top 10 users by contributions"
pprint.pprint(list(userContributions()))
print "============================================================"

print "Number of users having only 1 post"
pprint.pprint(list(singlepostusers()))
print "============================================================"

print "Total number of addresses"
pprint.pprint(countAddresses())
print "============================================================"

print "Addresses with no Street"
pprint.pprint(list(count_incomplete_addresses("street")))
print "============================================================"

print "Addresses with no postcode"
pprint.pprint(list(count_incomplete_addresses("postcode")))
print "============================================================"

print "Addresses with no House number"
pprint.pprint(list(count_incomplete_addresses("housenumber")))
print "============================================================"

print "Top 10 addresses by City"
pprint.pprint(list(addressGroupByCitySuburb()))
print "============================================================"