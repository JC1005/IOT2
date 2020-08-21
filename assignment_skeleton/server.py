from flask import Flask, render_template, jsonify,request

app = Flask(__name__)

import json
import dynamodb
import jsonconverter as jsonc

@app.route("/api/getdata",methods=['POST','GET'])
def apidata_getdata():
    if request.method == 'POST' or request.method == 'GET':
        try:
            #jsonc.data_to_json(
            data = {'chart_data': json.loads(jsonc.data_to_json(dynamodb.get_data_from_dynamodb())), 
             'title': "IOT Data"}            
            #data = data.replace("\"","'")
            print("before json loads")
            print(data)
            #dataj = json.loads(data)
            print()
            print("after json loads")
            #print(dataj)
            #return data
            return jsonify(data)
            #return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/")
def home():
    return render_template("index.html")


app.run(debug=True,host="0.0.0.0")
