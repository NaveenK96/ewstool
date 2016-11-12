import sqlite3 as sql
import urllib2
import json
import time

database = "Building.db"

def insert_data():
	response = urllib2.urlopen('https://my.engr.illinois.edu/labtrack/util_data_json.asp')
	data = response.read()
	data = json.loads(data)['data']

	with sql.connect(database) as con:
	    cur = con.cursor()
	    for lab in data:
	    	lab_name = ' '.join(lab['strlabname'].split(' ')[1:])
	    	if lab_name == '':
	    		lab_name = 'default'
	    	cur.execute("INSERT INTO Labs (LabName, InUse, Total, TS) VALUES (?,?,?,?)", (lab_name, lab['inusecount'], lab['machinecount'], time.time()))
	    con.commit()