"""
CS356 finalproject

A front end application that uploads files to VirusTotal via their public API.
Successful submissions are written to a cloudstore database
Requests to this API are restricted to 4 requests per minute.
"""
import requests as rqs
from datetime import datetime as dt
import flask, json,  sys
from flask import request, redirect
from flask.views import MethodView
from index import Index
from submissions import Submissions
import vtmodel

# Retrieving our VirusTotal public API key
from google.cloud import secretmanager
smclient = secretmanager.SecretManagerServiceClient()
sr = smclient.access_secret_version(name="projects/0000/secrets/VTKEY/versions/1")
VTKEY = sr.payload.data.decode("UTF-8")

app = flask.Flask(__name__)       # our Flask app
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 32 # 32MBytes maximum request size for safety

# Homepage where you can upload a file
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET", 'POST'])

# Page where you can view previous submissions made with this appliction
app.add_url_rule('/submissions/',
                 view_func=Submissions.as_view('submissions'),
                 methods=['GET'])

# This function handles file submissions to the VirustTotal API
@app.route("/submit_file", methods=["POST"])
def submit_file():
    model = vtmodel.get_model()

    file = request.files["file"]
    print(file, file=sys.stderr)

    headers = { 'x-apikey': VTKEY }
    payload = { 'file': file }
    response = rqs.post('https://www.virustotal.com/api/v3/files', headers=headers, files=payload)
    # Get json from response, load it into a dictionary
    rd = response.json()

    #if !(rd['e):
    model.insert(rd['data']['id'], file.filename, dt.now())
    return redirect("/")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
