# -*- coding: utf-8 -*-
""" 
audit.py 
This file will read the osm file into the memory using iterative parsing 
and check for the various auditing actions that will be performed

""" 

"""
Created on Tue Sep 08 10:17:26 2015

@author: ashutoshsingh
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "..\sample.osm"
#OSMFILE = "..\mumbai_india.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) #finding last word
parenthesis_re = re.compile(r'\([^)]*\)',re.IGNORECASE) #everthing with parenthesis
zipcode_re = re.compile(r'400\d\d\d', re.IGNORECASE) #zipcode according to mumbai


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# mapping to update the last word of street names found
mapping = { "St": "Street",
            "St.": "Street", 
            "Rd.": "Road",
            "Ave": "Avenue",
            "FOB" : "Footover Bridge",
             "(W)" : "(West)",
             "Rd"  : "Road",
             "Road": "Road",
             "Rd." : "Road",
             "stn" : "Station",
             "galli" : "Gali"
            }

#get the last word of the street name and check in expected. If not then add to dictionary
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m: 
        street_type = m.group()
        if street_type not in expected:
            #print street_type
            street_types[street_type].add(street_name)

			
#find if there is whitespace in the zip code ; then search for pattern. and add it			
def audit_zip_code(zip_types,zipcode):
    #remove any whitespace from the string
    if (' ' in zipcode) == True:
        #print zipcode
        zip_types[zipcode].add(zipcode)
        
        
    #search for the pattern of zipcode
    m = zipcode_re.search(zipcode)
    if not m:
        
        zip_types[zipcode].add(zipcode)
        #print zipcode

def is_zip_code(elem):
    return ((elem.attrib['k'] == 'addr:postcode')  or (elem.attrib['k'] == 'addr:zipcode') ) 

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    zip_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or  elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_zip_code(tag):
                    audit_zip_code(zip_types,tag.attrib['v'])

    return street_types,zip_types
    

#updating the streetnames
#get the last word and check for mapping ; if present replaces 
#if there is parenthesis in name then remove evertything inside it. They represent other names
def update_name(name, mapping):

    # YOUR CODE HERE
    m = street_type_re.search(name)
    if m:
        
        if m.group() in mapping.keys():
            name = re.sub(street_type_re, mapping[m.group()], name)

    #remove the parenthesis from the names
    m = parenthesis_re.search(name)        
    if m:
        name = re.sub(parenthesis_re, '', name)
            

    #return the updated name with title case and no whitespaces
    return name.title().strip()

#updating zip code 
#search according to local zipcode format 
#if not then 
# remove whitespace, replace o with zeros    
# 2digit zipcodes to be made 6 digit
# replacing first 3 digits with 400 in other cases
def update_zipcode(zipcode):
    m = zipcode_re.search(zipcode)
    
    if not m:
        #print zipcode        
        zipcode = zipcode.replace(' ' ,'') #remove whitespace in between
        zipcode = zipcode.replace('o', '0') #replace o with zeros
        
        #replace the 2 digit zipcodes with complete 
        if len(zipcode )== 2: #special case for 2 digits zip code.
            zipcode = '4000' + zipcode 
        elif len(zipcode) !=6 :
            #get the last 3 chars 
            zipcode = '400' + zipcode[-3:]
        
    return zipcode
        
    


def test():
    st_types,zip_types = audit(OSMFILE)
    #   assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    #change st_types with zip_types here when using zip code
    for zip_types,ways in zip_types.iteritems():
    #for st_type, ways in st_types.iteritems():
        for name in ways:
            #better_name = update_name(name, mapping)
            better_zip = update_zipcode(name)
            

                        
            #print name, "=>", better_name
            print name, "=>", better_zip
            

if __name__ == '__main__':
    test()