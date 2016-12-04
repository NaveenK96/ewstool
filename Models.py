import sqlite3 as sql
import urllib2
import json
from datetime import datetime, timedelta

database = "Building.db"

def get_building_address(building_name):
    with sql.connect(database) as con:
        cur = con.cursor()
        result = cur.execute("SELECT Address FROM Building WHERE BuildingName = (?);", (building_name,))
        con.commit()
        return result.fetchall()

def get_lab_details(lab_name):
    with sql.connect(database) as con:
        cur = con.cursor()
        result = cur.execute("SELECT Lab_Details FROM Building WHERE LabName = (?);", (lab_name,))
        con.commit()
        return result.fetchall()

def get_labs_from_building(building_name):
    with sql.connect(database) as con:
        cur = con.cursor()
        result = cur.execute("SELECT LabName FROM Building WHERE BuildingName = (?);", (building_name,))
        con.commit()
        return result.fetchall()

def get_total_from_lab(lab_name):
    with sql.connect(database) as con:
        cur = con.cursor()
        result = cur.execute("SELECT Total FROM Labs WHERE LabName = (?);", (lab_name,))
        con.commit()
        return result.fetchall()

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
            lab_name_split = lab['strlabname'].split(' ')
            building_name = lab_name_split[0]
            lab_name = ' '.join(lab_name_split[1:])
            if lab_name == '':
                lab_name = 'default'
            cur.execute("INSERT INTO Labs (BuildingName, LabName, InUse, Total, Year, Month, Day, Hour) VALUES (?,?,?,?,?,?,?,?)", (building_name, lab_name, lab['inusecount'], lab['machinecount'], year, month, day, hour,))
        con.commit()

def get_historical_data(lab_name):
    print('\n\n\nlab_name = ' + lab_name)
    total = 0
    num = 0
    average = [-1] * 24

    for j in range(0, 24):
        num = 0
        total = 0
        for i in range(0, 4):
            d = datetime.today() + timedelta(hours=j) - timedelta(days=7*(i+1))
            with sql.connect(database) as con:
                cur = con.cursor()
                result = cur.execute("SELECT InUse FROM Labs WHERE LabName = (?) AND Year = (?) AND Month = (?) AND Day = (?) AND Hour = (?);", (lab_name, d.year, d.month, d.day, d.hour,))
                con.commit()
            result = result.fetchall()
            if len(result) > 0:
                if j == 21:
                    print('j = ' + str(j) +', usage = ' + str(result[0][0]))
                total += result[0][0] 
                num += 1

        if num > 0:
            average[j] = total / num
            if j == 21:
                print 'total = ' + str(total)
                print 'num = ' + str(num)
                print 'average = ' + str(average[j])
                print ''
        # else:
            # print('No historical data available')

    return average
