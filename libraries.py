import json
import requests
import os

from flask import request
from flask import Flask, render_template

application = Flask(__name__)
app = application
libraries = []

@app.route("/static/search_libraries", methods=['POST'])
def get_libraries():
    libraries.clear()
    param = {}
    district = request.form['district']
    if (district != ""): 
        param['district'] = district
    computers = request.form['computers']
    if (computers != ""): 
        param['computers'] = computers
    wifi = request.form['wifi'].title()
    if (wifi != ""): 
        param['wifi'] = wifi

    # CODE FROM ASSIGNMENT 1:

    # display the welcome message if there are no parameters
    if (district == "" and computers == "" and wifi == ""): 
        return '[{“welcome_message”: “Welcome to Austin Libraries Information Web Application”}]'

    # gets personal apptoken
    apptoken = os.environ.get('APP_TOKEN')
    url = 'https://data.austintexas.gov/resource/tc36-hn4j.json?$$app_token=' + apptoken

    # retrieves data
    response = requests.get(
        url,
        params = (param)
        )

    # filters out key/value pairs to display
    for library in response.json(): 
        info = { 
            "Name": library['name'],
            "Phone": library['phone'],
            "Address": library['address']['human_address'],
            "District": library['district'] if 'district' in library.keys() else "N/A",
            "Computers": library['computers'] if 'computers' in library.keys() else "N/A",
            "Wifi": library['wifi'] if 'wifi' in library.keys() else "N/A"
        }
        libraries.append(info)

    return render_template('libraries.html')


@app.route("/libraries")
def return_libraries():
    return json.dumps(libraries)


@app.route("/")
def library_info_website():
    return render_template('index.html')

