# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:35:32 2015

@author: ashutoshsingh
"""

from pprint import pprint

def top_contributing_users(db):
    pipeline = [
            {"$group": { "_id": "$created.user" , "count": {"$sum": 1}}},
            {"$sort": { "count" : -1}},
            {"$limit": 1}
        ]
        
    print list(db.mumbai.aggregate(pipeline))

def single_entry_users(db):
    pipeline = [
            {"$group" : { "_id": "$created.user", "count": { "$sum": 1}}},
            {"$group" : { "_id": "$count" , "num_users": { "$sum" : 1}}}, 
            {"$sort" : {"_id" : 1}}, 
            {"$limit" : 1}    
        ]
        
    print list(db.mumbai.aggregate(pipeline))

#biggest religion by finding amenities 

def biggest_religion(db):
    pipeline = [
            {"$match" : {"amenity" : {"$exists" : 1}, "amenity" : "place_of_worship"}},
            {"$group" : {"_id" : "$religion" , "count" : {"$sum" : 1}}},
            {"$sort" : {"count" : -1}}
        ]
        
    pprint( list(db.mumbai.aggregate(pipeline)))
    
#what is None religion
def find_none_religion(db):
    pipeline = [
            {"$match" : { "amenity" : {"$exists" : 1 } , "amenity" : "place_of_worship"  ,"religion":None}},
            {"$project" : {"_id" : 0, "name" :1}},
            {"$limit" : 5 }
        ]
        
    pprint( list(db.mumbai.aggregate(pipeline)))
    
def find_top_10_amenities(db):
    pipeline = [
            {"$match" : {"amenity" : {"$exists":1}}},
            {"$group" : {"_id"  : "$amenity" , "count" :{"$sum" :1}}},
            {"$sort" : {"count" : -1}},
            {"$limit" : 10}
        ]
        
    pprint( list(db.mumbai.aggregate(pipeline)))

if __name__ == "__main__":

    from pymongo import MongoClient    
    client = MongoClient("mongodb://localhost:27017")
    
    db = client.maps
    #top_contributing_users(db)
    #single_entry_users(db)
    #biggest_religion(db)
    #find_none_religion(db)
    find_top_10_amenities(db)

    client.close()


