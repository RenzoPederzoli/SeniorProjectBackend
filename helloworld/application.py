#!flask/bin/python
import json
import time, os
from flask import Flask, Response, request, send_file   
from subprocess import run
from flask_cors import CORS

import optparse

application = Flask(__name__)
CORS(application)

def sendFileServer(f):
    return run(["scp", './helloworld/'+f, "student_guest@rvc.eng.miami.edu:/home/student_guest/"])

def getFileServer():
    time_limit = 15 # 20 sec from now.
    check_interval = 1 # seconds between checking for the file.

    now = time.time()
    last_time = now + time_limit

    while time.time() <= last_time:
        if run(["scp", "student_guest@rvc.eng.miami.edu:/home/student_guest/output.jpg", "./helloworld"]).returncode == 0:
            print('received output file')
            return 0
        else:
            time.sleep(check_interval)
    return 1;

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Helo World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/upload_file', methods=['GET', 'POST'])
def saveImage():
    f = request.files['file']
    f.filename = "test.jpg"
    f.save('./helloworld/'+f.filename)
    sendFileServer(f.filename)
    r = getFileServer()
    if r == 1:
        return send_file('error-img.png')
    else:
        return send_file('output.jpg')

if __name__ == '__main__':
    default_port = "80"
    default_host = "0.0.0.0"
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help=f"Hostname of Flask app {default_host}.",
                      default=default_host)

    parser.add_option("-P", "--port",
                      help=f"Port for Flask app {default_port}.",
                      default=default_port)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    application.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
