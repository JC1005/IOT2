from flask import Flask, render_template, jsonify, request,Response

import argparse
import sys

import json

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

from datetime import datetime
from playsound import playsound
from IOTAssignmentUtilitiesdorachua.MySQLManager import MySQLManager

gevent.monkey.patch_all()


app = Flask(__name__)

@app.route("/api/getdata",methods=['GET', 'POST'])
def apidata_getdata():
    try:
        bookingid = '51539607614.0'
        limit = 1000
        bookingid = "ALL"
        if 'bookingid' in request.form:        
            bookingid = request.form['bookingid']
        if 'datalimit' in request.form:
            limit = request.form['datalimit']       

        u='iotuser';pw='iotpassword';h='localhost';db='iotdatabase'
        mysqlm = MySQLManager(u,pw,h,db)
        mysqlm.connect()
		
        sql=f"SELECT MAX(datetimestart_value) FROM iotapp"
        datasql = {}            
        list_data = mysqlm.fetch_fromdb_as_list(sql,datasql)

        if len(list_data)>0:
            max_datetimestart_value = list_data[0]['MAX(datetimestart_value)']

            if bookingid == "ALL":
                sql=f"SELECT * FROM iotapp WHERE datetimestart_value=%(datetimestart_value)s ORDER BY datetime_value DESC"
                datasql = {"datetimestart_value": max_datetimestart_value}
            else:                
                sql=f"SELECT * FROM iotapp WHERE bookingid=%(bookingid)s AND datetimestart_value=%(datetimestart_value)s ORDER BY datetime_value DESC"
                datasql = {"bookingid": bookingid, "datetimestart_value": max_datetimestart_value}
        else:
            if bookingid == "ALL":
                sql=f"SELECT * FROM iotapp ORDER BY datetime_value DESC LIMIT {limit}"
                datasql = {}
            else:                
                sql=f"SELECT * FROM iotapp WHERE bookingid=%(bookingid)s ORDER BY datetime_value DESC"
                datasql = {"bookingid": bookingid}
                
        json_data = mysqlm.fetch_fromdb_as_json(sql,datasql)
        loaded_r = json.loads(json_data)
        data = {'chart_data': loaded_r, 'title': "IOT Data", 'chart_data_length': len(json_data)}

        mysqlm.disconnect()
        
        return jsonify(data)
        
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


@app.route("/multiple")
def multiple():
    return render_template('index_multiple.html')

@app.route('/buzzer',methods=['GET', 'POST'])
def buzzer():
    return "sound.wav"

	
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
   try:
        host = '0.0.0.0'
        port = 80
        parser = argparse.ArgumentParser()        
        parser.add_argument('port',type=int)
        
        args = parser.parse_args()
        if args.port:
            port = args.port
                
        http_server = WSGIServer((host, port), app)
        app.debug = True
        print('Web server waiting for requests')
        http_server.serve_forever()

        
   except:
        print("Exception while running web server")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
