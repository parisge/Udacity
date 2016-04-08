# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:40:42 2015

@author: GEP
"""

"""
Your task in this exercise has two steps:
- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
from pymongo import MongoClient
import re
import pprint
import phonenumbers as pn #pip install phonenumbers
import codecs
import json

#OSMFILE = "sample.osm"
OSMFILE = "athens_greece.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#"Liossion", "Polytehneiou", "Lempesi",
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
             "Trail", "Parkway", "Commons", "Λεωφόρος", "Πλατεία", "Οδός"]
city_exp = ["Athens", "Agios Stefanos", "Aigina","Alimos", "Glyfada", "Chaidari", "Ilioupolis", "Kifisia", 
            "Koropi", "Lavrio", "Marmaris", "Psychico", "Salamina", "Voula", "Vrilissia"]
city_map = {
            "Aegina":"Aigina",
            "Athen":"Athens",
            "Korvp;i":"Koropi",
            }
# UPDATE THIS VARIABLE
#Mapping has to sort in length descending.
mapping = { 
            "Ave":"Avenue",
            "St.": "Street",
            "Rd." : "Road",
            "N.":"North",
            "St" : "Street",
            "Leof.": "Leoforos",
            "Leof": "Leoforos",
            "road": "Road",
            "leof.": "Leoforos",
            "Str" : "Street",
            "Str." : "Street",
            "Liosion": "Liossion",
            "Λεωφορος": "Λεωφόρος",
            "Λεωφωρος": "Λεωφόρος",
            "Λεωφώρος": "Λεωφόρος",
            "Λεωφ.": "Λεωφόρος",
            "Λεωφ": "Λεωφόρος",
            "Πλατία": "Πλατεία",
            "Πλατ": "Πλατεία",
            "Πλατ.": "Πλατεία",
            "u'":"",
            "Οδ":"Οδός",
            "Οδ.":"Οδός",
            }
            
street_types = defaultdict(set)
zipcode_types = defaultdict(set)
city_types = defaultdict(set)
phone_types = defaultdict(set)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
    
def clean_street_name(street_name, mapping,street_types):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            street_name =  re.sub(street_type_re,mapping[street_type] , street_name)
            street_types[street_type].add(street_name)
        #if street_type not in expected:
            #street_types[street_type].add(street_name)
    return street_name	

def clean_city(city_name, city_map, city_types):
    m = street_type_re.search(city_name)
    if m:
        city_type=m.group()
        if city_type in city_map:
            city_name= re.sub(street_type_re,city_map[city_type] , city_name)
            city_types[city_type].add(city_name)
        #if city_type not in city_exp:
            #city_types[city_type].add(city_name)
        
    return city_name

    
def clean_phone(key, value, phone_types):
    #Athens phone numbers have a 3 digit area code(210) following for a 7 digit number
    #if only 7 digits are supplied, I assume it's missing the Athens area code
     
    list_of_phone_num = []
    phone_numbers = value.split(";")
    for number in phone_numbers:
            
        number = number.replace("+30","").lstrip().rstrip()   #strip out country code so that area code can be prefixed if required 
        m=re.match(r"[^0-9]",number)
        if m:
            phone_types[number].add(value)
        numbers_only = re.sub("[^0-9]", "", value)
        
        if len(numbers_only) == 7 :
           number = "210" +  number
        
        try:
           phone_num = pn.parse(value,"GR")
           if pn.is_valid_number(phone_num):
               cleaned = pn.format_number(phone_num,pn.PhoneNumberFormat.INTERNATIONAL)
               list_of_phone_num.append(cleaned)
           
        except:
            pass
    return list_of_phone_num

    
def clean_address(key, value,street_types,city_types, zipcode_types):
    key =  key.replace("addr:","")     
    if key == "street":
        value = clean_street_name(value,mapping,street_types)
    elif key == "postcode":
        value = re.sub("[^0-9]", "", value)
        if len(value) != 5:
            zipcode_types[value].add(value)
    elif key == "city":
        value = clean_city(value,city_map, city_types)
    return key, value

def auditprocess(elem):
    node = {}
    if elem.tag == "node" or elem.tag == "way":
        address = {}
        created = {}
        pos = []
        node_refs = []
        
        for tag in elem.iter("tag"):
            value = tag.attrib['v']
            key = tag.attrib['k']
            if problemchars.search(key) or key.count(":") > 1:
                pass
            else: 
                if key.startswith("addr:"):                    
                    key, value = clean_address(key, value, street_types, city_types, zipcode_types)
                    address[key.replace("addr:","")] = value 
                if key == "phone":
                    value = clean_phone(key, value, phone_types)      
                node[key] = value
            #if is_street_name(tag):
            #    audit_street_type(street_types, tag.attrib['v'])

        
        #build node_regs for way tag
        if elem.tag == "way":
            for tag in elem.iter("nd"):
                node_refs.append(tag.attrib["ref"])
            if len(node_refs) > 0:
                node["node_refs"] = node_refs
        
        #read attributes of tag
        for attribute in elem.items():
            key = attribute[0]
            value =  attribute[1]
            if key in CREATED:
                created[key] = value
            elif key == 'lat':
                pos.insert(0, float(value))
            elif key == 'lon':
                pos.append(float(value))
            else:
                node[key] = value
                
        node["created"] = created
        node["type"] = elem.tag
        if len(pos) > 0 :
            node["pos"] = pos
        
        if len(address) > 0:
            node["address"] = address
        
        #pprint.pprint(node)

         
    #pprint.pprint(dict(street_types))
    #pprint.pprint(dict(city_types))
    #pprint.pprint(dict(zipcode_types))
    #pprint.pprint(dict(phone_types))
      
    return node

def process_map(file_in, pretty):
        # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = auditprocess(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    
def update_name(name, mapping):
    """
    Fixed abreviate name so the name can be uniform.
    
    The reason why mapping in such particular order, is to prevent the shorter keys get first.
    """
    for key in mapping:
        if name.find(key) != -1:         
            name = name.replace(key,mapping[key])
            break

    return name


def test():
    data = process_map(OSMFILE,True)
    
    client = MongoClient('localhost',27017)
    db = client.openstreetdata

    pprint.pprint(data[0:10])
    #pprint.pprint(dict(st_types))
    #print st_types
    if "map" in db.collection_names():
        db.drop_collection("map")
    
    db.map.insert_many(data)
    
    print db.map.count()  

if __name__ == '__main__':
    test()