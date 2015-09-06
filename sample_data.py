# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:00:07 2015

@author: ashutoshsingh
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client.maps;


##get all the postal codes in decreasing order of count
#pipeline = [ {"$match":{"address.postcode" : {"$exists":1}}},
#             {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}},
#             {"$sort" :{"count" :-1 }} ]
             
#now clean the postal codes main errors are 
#1. spaces in between 
#2. not in 6 characters
#doesn't start with 400
# contains alphabetic characters. 

##pipeline to get most number of amenity types
#pipeline = [
#            {"$match": {"amenity" : {"$exists":1}}},
#            {"$group": {"_id": "$amenity" , "count": {"$sum": 1}}},
#            {"$sort" : {"count" : -1}}
#    ]      
#                                                


##Uncomment to get the top most religion node 
#pipeline = [
#        {"$match": { "amenity" : "place_of_worship"} },
#        {"$group": {"_id": "$religion" ,"count" : {"$sum":1}}},
#        {"$sort" : {"count" : -1}}  
#        
#    ]

##getting the total number of users who edited the map
#print  len(db.mumbai.distinct("created.user"))


##getting the top user
#pipeline = [
#        {"$group": { "_id" : "$created.user" , "count" : {"$sum" : 1 }}},
#        {"$sort": {"count" :-1}},
#        {"$limit" : 1}
#    ]


##getting all the road names to check of any discrepency
pipeline = [
        {"$match" : {"address.street" :  { "$exists"  : 1}}},        
        {"$project" : {"name" : "$address.street" ,"_id" : 0}},
        {"$group"  : {"_id" : "$name" } }
        
            ]

cursor   =  db.mumbai.aggregate(pipeline)

# for checking the pincodes
#for document in cursor:
#      pincode = document["address"]["postcode"]
#      if len(pincode ) > 6 or  pincode[0] != "4" :
#          print document["address"]["postcode"]
#


#print cursor.count()
for document in cursor:
      print document




client.close()