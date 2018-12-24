# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 03:22:18 2018

@author: Manu kumar
"""

# Haversine formula in Python
# Based on snippet by Wayne Dyck for calculation of dist. between latitude longitude pairs
# https://gist.github.com/rochacbruno/2883505

import math

def distance(origin, destination):

    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 * 1000 # in meters

    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    
    dlat = math.radians((lat2) - (lat1))
    dlon = math.radians((lon2) - (lon1))
    
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d