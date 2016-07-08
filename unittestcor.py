# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:41:55 2016

@author: miche
"""

import socket
import pytest
import unittest

adres = [['Diepenbrocklaan', '28', '4614BM', 'BERGEN OP ZOOM'], 
        ['Leeuwarderweg', '61', '9005ND', 'WERGEA'], 
        ['Blondeelstraat', '116', '3067VB', 'ROTTERDAM'], 
        ['Kanaalweg West', '62', '7691CA', 'BERGENTHEIM'], 
        ['Maltezerplein', '19', '1961JC', 'HEEMSKERK']]

adresCor = []
def adresGeo(lst):
    from time import sleep
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(500)
    for item in lst:
         location = geolocator.geocode(item, timeout=500)
         if location:
             locatieCor = [location.latitude, location.longitude]
             adresCor.append(locatieCor)
             sleep(1)
         else:
             adresCor.append("onbekend")
             sleep(1)
adresGeo(adres)

def test_method1():
    assert adresCor == [[51.5041512, 4.2945045], 
                        [53.152257, 5.8414487], 
                        [51.9435768, 4.5440299], 
                        [52.5286441, 6.6204505], 
                        [52.5105812, 4.6686622]], 'De coordinaten zijn niet correct'

# Run in het Anaconda prompt scherm 
# de volgende tekst: py.test unittestcor.py