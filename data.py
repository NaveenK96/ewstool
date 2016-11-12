#!/usr/bin/python

import urllib2
import json

response = urllib2.urlopen('https://my.engr.illinois.edu/labtrack/util_data_json.asp')
data = response.read()
data = json.loads(data)['data']
for lab in data:
	print lab['strlabname'] + ': ' + str(lab['inusecount']) + '/' + str(lab['machinecount'])


response = urllib2.urlopen('http://www.gps-coordinates.net/api/dcl')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/siebl')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/eceb')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/eh')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/espl')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/far')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/par')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/grainger')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/mel')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/rec')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/sdrp')
print(response.read())
response = urllib2.urlopen('http://www.gps-coordinates.net/api/tb')
print(response.read())