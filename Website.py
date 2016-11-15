from flask import Flask, request, render_template, url_for, jsonify
from collections import OrderedDict
from urllib2 import urlopen
from json import loads, dumps
from datetime import datetime
from Models import *
from sqlite3 import connect
import pygal

app = Flask(__name__)

@app.context_processor
def inject_static():
    css_urls = [url_for('static', filename='font-awesome-4.7.0/css/font-awesome.min.css'), url_for('static', filename='bootstrap.min.css')]
    js_urls = [url_for('static', filename='jquery-3.1.1.min.js'), url_for('static', filename='tether.min.js'), url_for('static', filename='bootstrap.min.js')]
    return dict(css_urls=css_urls,
                js_urls=js_urls,
                title="the bourne interface")

@app.route('/<name>', methods=['GET'])
def prediction(name = None):
    print name
    building_name = "DCL"
    labs = get_labs_from_building(building_name)
    charts = {}
    building_address = get_building_address(building_name)
    for lab in labs:
        lab = str(lab[0])
        lab_details = get_lab_details(lab)
        data = get_historical_data(lab)
        bar_chart = pygal.Bar(width=1100, height=600, range=(0, 70))
        bar_chart.title = "Next 24 hour prediction for " + lab
        bar_chart.add('Usage', data)
        xlabels = []

        for i in range(datetime.now().hour, datetime.now().hour+24):
            suffix = ''
            if i%24 < 12:
                suffix = ' AM'
            else:
                suffix = ' PM'
            if i%12 == 0:
                xlabels.append('12' + suffix)
            else:
                xlabels.append(str(i%12) + suffix)
        bar_chart.x_labels = xlabels
        charts[lab] = (str(bar_chart.render()).decode('utf-8'), lab_details[0][0].split('|'))
    # return Response(response=bar_chart.render(), content_type='image/svg+xml')
    return render_template('details.html',
                            result=charts,
                            building_name=building_name,
                            building_address=building_address,
                            title=name + " - the bourne interface")

@app.route('/', methods=['GET', 'POST'])
def index():
    css_urls = [url_for('static', filename='font-awesome-4.7.0/css/font-awesome.min.css'), url_for('static', filename='bootstrap.min.css'), url_for('static', filename='index.css')]
    js_urls = [url_for('static', filename='jquery-3.1.1.min.js'), url_for('static', filename='tether.min.js'), url_for('static', filename='bootstrap.min.js'), url_for('static', filename='index.js')]

    buildings = getBuildingData()

    return render_template('index.html',
                            buildings=buildings,
                            css_urls=css_urls,
                            js_urls=js_urls)

def getBuildingData():
    _buildings = loads(urlopen('https://my.engr.illinois.edu/labtrack/util_data_json.asp').read())['data']
    buildings = OrderedDict()
    for lab in _buildings:
        lab_name = lab['strlabname'].split(" ", 1)
        building = lab_name[0]
        del lab_name[0]
        lab_name = " ".join(lab_name)
        if lab_name == '':
            lab_name = 'Default'
        if building not in buildings:
            buildings[building] = dict()
        if 'labs' not in buildings[building]:
            buildings[building]['labs'] = OrderedDict()
        if lab_name not in buildings[building]['labs']:
            buildings[building]['labs'][lab_name] = dict()
        if 'inuse' not in buildings[building]:
            buildings[building]['inuse'] = 0
        if 'total' not in buildings[building]:
            buildings[building]['total'] = 0
        buildings[building]['labs'][lab_name]['inuse'] = lab['inusecount']
        buildings[building]['inuse'] += lab['inusecount']
        buildings[building]['labs'][lab_name]['total'] = lab['machinecount']
        buildings[building]['total'] += lab['machinecount']

    with connect("Building.db") as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `building_info`")
        for item in cursor.fetchall():
            buildings[item[0]]['long_name'] = item[1]
            buildings[item[0]]['latitude'] = item[2]
            buildings[item[0]]['longitude'] = item[3]
            buildings[item[0]]['address'] = item[4]
            buildings[item[0]]['hours'] = item[5]
    return buildings

if __name__ == '__main__':
    # app.run()
    app.run(debug=True, ssl_context=('server.crt', 'server.key'))
