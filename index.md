Project 3 : Data Wrangling with MongoDB
===========================
Ashutosh Singh
--------------

###Map Area: Mumbai, Maharashtra, India


####1. History and Motivation

I chose the Mumbai area as I am residing here for the past 2 years and wanted to explore more in this area. Also I wanted to look at the data quality as not many of colleagues have heard of Open Street Maps and not many people here are so much educated that we can update the maps and improve the data quality (My personal perception before starting this project).

Also Mumbai is not a planned city. So the basic analysis of street names as shown in the course will not work out of the box here.  Here we have many names of street and the street names do not only have “road” or other predefined structure in them. Let’s take a look at the data.


Lets take a look at different type of street names in Mumbai. The pipe line is this
```pipeline = [
{ "$match" : {"address.street" : { "$exists" : 1}}},
{ "$project" : {"name" : "$address.street" ,"_id" : 0}},
]```

The output is as follows


####3. Overview of the Data
This section contains the basic statistics about the dataset and the queries used to fetch them

#####File Sizes

>mumbai_india.osm :  335773 kB

>mumbai_india.json :  395533 kB


#####Number of documents :
`db.mumbai.find()`
>1880457

#####Number of nodes :
`db.mumbai.find({type:”node”}).count()`
>1674702

#####Number of ways :
`db.mumbai.find({type:{“way”}).count()`
>205554

Number of unique users
>db.mumbai.distinct(“created.user”).length
1086

#####Top Contributing user
```
db.mumbai.aggregate( [
{"$group": { "_id": "$created.user" , "count": {"$sum": 1}}},
{"$sort": { "count" : -1}},
{"$limit": 1}
] )
```

>[{u'count': 71060, u'_id': u'parambyte'}]

#####Users with single edit
```
db.mumbai.aggrefate([
{"$group" : { "_id": "$created.user", "count": { "$sum": 1}}},
{"$group" : { "_id": "$count" , "num_users": { "$sum" : 1}}},
{"$sort" : {"_id" : 1}},
{"$limit" : 1}
] )
```

>[{u'num_users': 205, u'_id': 1}]
