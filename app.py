# coding = UTF-8
# -*- coding: cp936 -*-


from flask import Flask,jsonify,abort,request
from flask import make_response
import logging, httplib, urllib,os
import json, requests
import cloudinary
from random import choice
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename


log = logging.getLogger(__name__)


app = Flask(__name__)

cloudinary.config(cloud_name = "k3ith", api_key = "727583551141279", api_secret = "8gMNUCmI3uLzTNZXjbLV744I0Gc")


def getEmotionScore(image):
    imageUrl = cloudinary.uploader.upload(image)['secure_url']
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'db7f098cfc6544f799e25b12c103aa55',
    }
    params = urllib.urlencode({
    })
    body = "{ 'url': '"+imageUrl+"' }"
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    try:
        data = json.loads(response.read())[0]['scores']
    except Exception:
        print "no face"
    else:
        return data
    conn.close()


def getEmotionKey(image):
    d = getEmotionScore(image)
    keys = sorted(d, key=lambda k: d[k])
    count = len(keys)
    return keys[count-1]


def getMusicUrl(keyword):
    data = {'keywords': keyword}
    resp = requests.get('http://enigmatic-refuge-10196.herokuapp.com/search', params=data, headers=None, cookies=None)
    songsList = json.loads(resp.content)['result']['songs']
    idList = []
    for song in songsList:
        idList.append(song['id'])
    return choice(idList)




@app.route('/api/emotionkey', methods=['POST'])
def createEmotionKey():
    if not request.json or not 'image' in request.json:
        abort(400)
    logging.log(request.json['image'],'body')
    keywords = getEmotionKey(request.json['image'])
    return keywords


@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.getcwd()+"/static", "current_image.jpg"))
            tasks = []
            return jsonify({'tasks': tasks})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}),404)




@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    print getMusicUrl(u'海阔天空')

    # print getEmotionKey('https://i.pinimg.com/736x/dd/21/a5/dd21a5719f50d914faf50c7b01c00a7f--taylor-marie-hill-taylor-hill-face.jpg')
    # app.run()
