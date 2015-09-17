Project 3 : Data Wrangling with MongoDB
===========================
Ashutosh Singh
--------------
**Table of Contents**

- [Project 3 : Data Wrangling with MongoDB](#)
	- [Ashutosh Singh](#)
		- [Map Area: Mumbai, Maharashtra, India](#)
			- [1. History and Motivation](#)
			- [3. Overview of the Data](#)
				- [File Sizes](#)
				- [Number of documents :](#)
				- [Number of nodes :](#)
				- [Number of ways :](#)
				- [Top Contributing user](#)
				- [Users with single edit](#)
		- [Additional Analysis](#)
			- [Places of Worship / Religion](#)
			- [Top 10 Amenities](#)


###Map Area: Mumbai, Maharashtra, India


####1. History and Motivation

I chose the Mumbai area as I am residing here for the past 2 years and wanted to explore more in this area. Also I wanted to look at the data quality as not many of colleagues have heard of Open Street Maps and not many people here are so much educated that we can update the maps and improve the data quality (My personal perception before starting this project).

Also Mumbai is not a planned city. So the basic analysis of street names as shown in the course will not work out of the box here.  Here we have many names of street and the street names do not only have “road” or other predefined structure in them. Let’s take a look at the data.


Lets take a look at different type of street names in Mumbai. The pipe line is this
```
pipeline = [
{ "$match" : {"address.street" : { "$exists" : 1}}},
{ "$project" : {"name" : "$address.street" ,"_id" : 0}},
]
```

The output is as follows


####3. Overview of the Data
This section contains the basic statistics about the dataset and the queries used to fetch them


#####File Sizes

>mumbai_india.osm :  335773 kB

>mumbai_india.json :  395533 kB


#####Number of documents :

`>1880457`

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

###Additional Analysis

#### Places of Worship / Religion
India is a mixture of religions,languages and cultures. Lets take a look at the places of worship in the city as sorted order.

```python
 pipeline = [
            {"$match" : {"amenity" : {"$exists" : 1}, "amenity" : "place_of_worship"}},
            {"$group" : {"_id" : "$religion" , "count" : {"$sum" : 1}}},
            {"$sort" : {"count" : -1}}
        ]

 pprint( list(db.mumbai.aggregate(pipeline)))

```
>[{u'_id': u'hindu', u'count': 128},<br>
 {u'_id': u'muslim', u'count': 97},<br>
 {u'_id': u'christian', u'count': 58},<br>
 {u'_id': None, u'count': 51},<br>
 {u'_id': u'buddhist', u'count': 14},<br>
 {u'_id': u'jain', u'count': 9},<br>
 {u'_id': u'zoroastrian', u'count': 9},<br>
 {u'_id': u'sikh', u'count': 6},<br>
 {u'_id': u'jewish', u'count': 4},<br>
 {u'_id': u'hare_krishna', u'count': 1},<br>
 {u'_id': u'sikhs', u'count': 1}]<br>

As found, there are 7 religious places found. The most pupular religion is hindu and then muslim also represented in the india's demographic data. Now few places of worship don't have a religion field in them. Printing them we get
```
 pipeline = [
            {"$match" : { "amenity" : {"$exists" : 1 } , "amenity" : "place_of_worship"  ,"religion":None}},
            {"$project" : {"_id" : 0, "name" :1}},
            {"$limit" : 5 }
        ]

    pprint( list(db.mumbai.aggregate(pipeline)))
```
>[{u'name': u'PANCHAMUKHI SRI HANUMAN MANDIR'},<br>
 {u'name': u'Nuri Baba Darga'},<br>
 {u'name': u'Saibaba Mandir'},<br>
 {u'name': u'Shiv Temple'},<br>
 {u'name': u'Don Bosco Church'}]

In the top 5 items we have 1 church, 3 temples and a dargah(muslim place of worship)
So it looks like the entries for these are incomplete and can be done by editing each place manually


#### Top 10 Amenities

First take a look at the top 10 amenities
```
 pipeline = [
            {"$match" : {"amenity" : {"$exists":1}}},
            {"$group" : {"_id"  : "$amenity" , "count" :{"$sum" :1}}},
            {"$sort" : {"count" : -1}},
            {"$limit" : 10}
        ]

 pprint( list(db.mumbai.aggregate(pipeline)))
 ```
 >[{u'_id': u'place_of_worship', u'count': 378},<br>
 {u'_id': u'restaurant', u'count': 267},<br>
 {u'_id': u'school', u'count': 244},<br>
 {u'_id': u'bank', u'count': 228},<br>
 {u'_id': u'hospital', u'count': 150},<br>
 {u'_id': u'fuel', u'count': 124},<br>
 {u'_id': u'parking', u'count': 122},<br>
 {u'_id': u'bus_station', u'count': 114},<br>
 {u'_id': u'cafe', u'count': 114},<br>
 {u'_id': u'college', u'count': 96}]

Well, it looks like we have more places of worship than we have schools and hospitals. There may be a bias here that schools are marked by the local users whereas we know of places of worship which are far away. So many users know of religious places than they know of schools and hospitals.
