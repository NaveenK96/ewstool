from flask import Flask, request, render_template, url_for, jsonify, make_response
from collections import OrderedDict, defaultdict
from datetime import datetime
from Models import *
from json import loads
import sqlite3
import pygal
from flask import Response

app = Flask(__name__)

@app.context_processor
def inject_static():
    return dict(css_url=url_for('static', filename='styles.css'),
                js_url=url_for('static', filename='index.js'),
                title="the bourne interface")

@app.route('/<name>', methods=['GET'])
def prediction(name=None):
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
    return render_template('details.html', result=charts, building_name=building_name, building_address=building_address)

@app.route('/', methods=['GET', 'POST'])
def index():
    con = sqlite3.connect("Building.db")
    cursor = con.cursor()

    if request.method == 'GET':
        response = urllib2.urlopen('https://my.engr.illinois.edu/labtrack/util_data_json.asp')
    	otherdata = response.read()
    	otherdata = json.loads(otherdata)['data']
        cursor.execute("SELECT `BuildingName`, `Latitude`, `Longitude` FROM `Building` GROUP BY `BuildingName`")
        buildings = list()
        for item in cursor.fetchall():
            buildings.append({'name':item[0], 'lat':item[1], 'lng':item[2]})

        return render_template('index.html', data=buildings, otherdata=otherdata)

    _labs = dict()
    cursor.execute("SELECT `LongName`, Labs.LabName, `InUse`, `Total`, `Latitude`, `Longitude` FROM `Labs` INNER JOIN `Building` ON Labs.LabName = Building.LabName ORDER BY Labs.ID DESC LIMIT 26")
    for item in cursor.fetchall():
        if not str(item[0]) in _labs:
            _labs[str(item[0])] = dict()
        _labs[str(item[0])][str(item[1])] = {'lab': str(item[1]), 'inuse': item[2], 'total': item[3], 'lat': item[4], 'lng': item[5]}

    labs = OrderedDict()
    for item in sorted(_labs.keys()):
        labs[item] = _labs[item]

    favorites = request.form.get('favorites')
    building = request.form.get('building')
    lab = request.form.get('lab')
    option = request.form.get('option')

    if not favorites:
        favorites = dict()
    else:
        favorites = loads(favorites)

    if building and option == 'ADD':
        lab = lab.split(":", 1)[0]
        if building not in favorites:
            favorites[building] = list()
        favorites[building].append(lab)

    if building and option == 'REMOVE':
        lab = lab.split(":")[1].lstrip(" ")
        favorites[building].remove(lab)
        if not favorites[building]:
            del favorites[building]

    to_del = list()
    for item in favorites:
        for thing in favorites[item]:
            to_del.append([item, thing])

    _favorites = dict()
    for item in to_del:
        if item[0] not in _favorites:
            _favorites[item[0]] = dict()
        _favorites[item[0]][item[1]] = labs[item[0]][item[1]]
        del labs[item[0]][item[1]]

    html = ""
    if _favorites:
        html += """<div class="panel panel-info"><div class="panel-heading"><h1 class=\"panel-title\">Favorites</h1></div>"""
        for item in enumerate(_favorites):
            num = str(item[0])
            item = item[1]
            for thing in _favorites[item]:
                html += """<div class=\"panel-body\"><a><div><div class=\"hidden\" style=\"display: none\">%s</div><div class=\"lab\">%s</div><span class=\"fa fa-star pull-right\" title=\"Unfavorite\"></span></div></a></div>""" % (str(_favorites[item][thing]['lat']) + ',' + str(_favorites[item][thing]['lng']) + "," + item + ",", item + ": " + _favorites[item][thing]['lab'] + ": " + str(_favorites[item][thing]['inuse']) + " / " + str(_favorites[item][thing]['total']))
        html += """</div>"""

    for item in enumerate(labs):
        num = str(item[0])
        item = item[1]
        if labs[item]:
            html += """<div class=\"panel panel-default\"><div class=\"panel-heading\" role=\"tab\" id=\"%s\"><h4 class=\"panel-title\"><a role=\"button\" data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#collapse%s\" aria-expanded=\"true\" aria-controls=\"collapse%s\">%s</a></h4></div><div id=\"collapse%s\" class=\"panel-collapse collapse out\" role=\"tabpanel\" aria-labelledby=\"%s\">""" % ('-'.join(item.split(' ')), num, num, item, num,'-'.join(item.split(' ')))
        for thing in labs[item]:
            html += """<div class=\"panel-body\"><a><div><div class=\"hidden\" style=\"display: none\">%s</div><div class=\"lab\">%s</div><span class=\"fa fa-star-o pull-right\" title=\"Favorite\"></span></div></a></div>""" % (str(labs[item][thing]['lat']) + ',' + str(labs[item][thing]['lng']) + "," + item + ",", labs[item][thing]['lab'] + ": " + str(labs[item][thing]['inuse']) + " / " + str(labs[item][thing]['total']))
        html += """</div></div>"""

    return jsonify({'html':html, 'favorites':favorites})

if __name__ == '__main__':
    # app.run()
    app.run(debug=True, ssl_context=('server.crt', 'server.key'))
