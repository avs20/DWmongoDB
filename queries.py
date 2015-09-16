# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:35:32 2015

@author: ashutoshsingh
"""

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

if __name__ == "__main__":

    from pymongo import MongoClient    
    client = MongoClient("mongodb://localhost:27017")
    
    db = client.maps
    #top_contributing_users(db)
    single_entry_users(db)



