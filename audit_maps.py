# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 10:54:11 2015

@author: ashutoshsingh
"""

import re
from pprint import pprint
import json 
import audit
from collections import defaultdict

    

#the json file to audit 
jsonFile = 'mumbai_india.osm.json'

#Look for the non whitespace character at the end including .
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#Look for the commas in the  string and remove everythig from last comma in string. 
street_type2_re = re.compile(r',',re.IGNORECASE)

expected = ["Street", "Avenue",  "Drive", "Court", "Place", "Square", "Lane", "Road", "Lane" 
            "Trail", "Parkway", "Commons", "Road", "Marg", "Chawl", "Chowk", "Galli", "Path", "Nagar",]

mapping = {
    'road': 'Road',
    'path': 'Path',
    'nagar': 'Nagar',
    'chawl': 'Chawl',
    

}

   
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            print street_type
            street_types[street_type].add(street_name)

def audit_json(jsonfile):
    street_types = defaultdict(set)
    
    with open(jsonfile) as f:
        for line in f:
            node = json.loads(line)
            if 'address' in  node and 'street' in node['address'] :
                mstr =  node['address']['street']
                mstr = mstr.replace('(','')
                mstr = mstr.replace(')','')
                print mstr
                comma = mstr.rfind(',')     
                if comma != -1 :
                    audit_street_type(street_types,mstr[:comma])
                else :
                    audit_street_type(street_types,mstr)
                
            
    return street_types
    
    
st_types = audit_json(jsonFile)
pprint(dict(st_types))