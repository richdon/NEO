# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 19:21:20 2021

@author: richa
"""
"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
import pathlib

from models import NearEarthObject, CloseApproach


here = pathlib.Path('.')

neo_csv_path = here.absolute() / 'data'/ 'neos.csv'

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    
    neo_lst = []
    neo_keys = ['pdes', 'name', 'pha', 'diameter']
    with open(neo_csv_path, 'r') as infile:
         reader = csv.DictReader(infile)
         for element in reader:
             neo_dict1 = {k : v for k, v in element.items() if k in neo_keys}
             neo_lst.append(neo_dict1)
    
        
    neo_obj_lst = []
        
    for neo in neo_lst:
        neo_obj_lst.append(NearEarthObject(designation = neo['pdes'], name = neo['name'],
                                   diameter = neo['diameter'], hazardous = neo['pha']))   
    return neo_obj_lst
    
###############################################################################    

cad_json_path = here.absolute() / 'data' / 'cad.json'

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    approach_lst = []
    
    with open(cad_json_path, 'r') as infile:
        data = json.load(infile)
        
        for val in data['data']:
            approach = dict(zip(data['fields'], val))
            approach_lst.append(approach)
        
        
    ca_obj_lst = []   
    for ca in approach_lst:
        ca_obj_lst.append(CloseApproach(des = ca['des'], time = ca['cd'],
                                 distance = ca['dist'], velocity = ca['v_rel']))
    return ca_obj_lst
