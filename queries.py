# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:35:32 2015

@author: ashutoshsingh
"""

"""
This file contains the addition section queries from the project report
"""

from pprint import pprint

#find top contributing users
def top_contributing_users(db):
    pipeline = [
            {"$group": { "_id": "$created.user" , "count": {"$sum": 1}}},
            {"$sort": { "count" : -1}},
            {"$limit": 1}
        ]
        
    print list(db.mumbai.aggregate(pipeline))

#total number of users who have made edit only once
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
    
#what is the name of the places of worship where religion is not mentioned
def find_none_religion(db):
    pipeline = [
            {"$match" : { "amenity" : {"$exists" : 1 } , "amenity" : "place_of_worship"  ,"religion":None}},
            {"$project" : {"_id" : 0, "name" :1}},
            {"$limit" : 5 }
        ]
        
    pprint( list(db.mumbai.aggregate(pipeline)))
    
#the top 10 types of amenities
def find_top_10_amenities(db):
    pipeline = [
            {"$match" : {"amenity" : {"$exists":1}}},
            {"$group" : {"_id"  : "$amenity" , "count" :{"$sum" :1}}},
            {"$sort" : {"count" : -1}},
            {"$limit" : 10}
        ]
        
    pprint( list(db.mumbai.aggregate(pipeline)))
    
#aggregate the number of edits first by year and then by month    
def find_editing_month_year(db):
    pipeline = [
            { "$group" : { "_id" : 
                    {"year" : "$created.year" ,
                     "month" :"$created.month"
                    },                     
                     "editCount" : {"$sum":1}}
            },
            { "$group" : { "_id" : "$_id.year",
                            "month" : {
                                    "$push" : {
                                            "month" : "$_id.month",
                                            "edits" : "$editCount"
                                        },
                                    },
                            "count": {"$sum": "$editCount"}
                          }},
            {"$sort" : {"count" : -1} },
            {"$limit" : 1            }       
        ]
    pprint( list(db.mumbai.aggregate(pipeline)))
    
#month in which most edits happened
def find_most_active_month(db):
    pipeline = [
            {"$group" :{ "_id" : "$created.month" , "count" : {"$sum" :1}}},
            {"$sort" : {"count" : -1}},
            {"$limit":2}    
        ]
    pprint( list(db.mumbai.aggregate(pipeline)))
    
#total number of buildings	
def find_buildings(db):
    pipeline = [
        {"$match" : {"building" : {"$exists" : 1}, "name" : {"$exists" :1}}},
        {"$group": {"_id" : "$building" , "count" :{"$sum" :1} }}  
    
    ]    
    
    pprint( list(db.mumbai.aggregate(pipeline)))
    
if __name__ == "__main__":

    from pymongo import MongoClient    
    client = MongoClient("mongodb://localhost:27017")
    
    db = client.maps
    top_contributing_users(db)
    single_entry_users(db)
    biggest_religion(db)
    find_none_religion(db)
    find_top_10_amenities(db)
    top_areas_of_worship(db)
    find_editing_month_year(db)
    find_most_active_month(db)
    find_buildings(db)

    client.close()


