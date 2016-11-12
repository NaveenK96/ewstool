import sqlite3 as sql
import urllib2
import json
from datetime import datetime, timedelta

database = "Building.db"

def insert_data():
	response = urllib2.urlopen('https://my.engr.illinois.edu/labtrack/util_data_json.asp')
	data = response.read()
	data = json.loads(data)['data']

	with sql.connect(database) as con:
	    cur = con.cursor()
	    year = datetime.now().year
	    month = datetime.now().month
	    day = datetime.now().day
	    hour = datetime.now().hour
	    for lab in data:
	    	lab_name = ' '.join(lab['strlabname'].split(' ')[1:])
	    	if lab_name == '':
	    		lab_name = 'default'
	    	cur.execute("INSERT INTO Labs (LabName, InUse, Total, Year, Month, Day, Hour) VALUES (?,?,?,?,?,?,?)", (lab_name, lab['inusecount'], lab['machinecount'], year, month, day, hour))
	    con.commit()

insert_data()