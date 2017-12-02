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


# emotion api
def getEmotionScore(image):
    logging.log(logging.DEBUG, "getEmotionScore")
    imageUrl = cloudinary.uploader.upload(image)['secure_url']
    logging.log(logging.DEBUG, imageUrl)
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'af2476d398aa45d7b7386a4591b83ff7',
    }
    params = urllib.urlencode({
    })
    body = "{ 'url': '"+imageUrl+"' }"
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    # logging.log(logging.DEBUG, "response = " + response)
    data =response.read()

    # logging.log(logging.DEBUG, json.loads(response))
    score = json.loads(data)[0]['scores']
    return score
    # logging.log(logging.DEBUG, jsonify(data= data))
    conn.close()


# get score
def getEmotionKey(image):
    d = getEmotionScore(image)
    print d
    keys = sorted(d, key=lambda k: d[k])
    count = len(keys)
    return keys[count-1]


# http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=%E7%8E%8B%E5%8A%9B%E5%AE%8F&page=1&pagesize=20&showtype=1
# http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword=sad&page=1&pagesize=10
# search keyword
def search(keyword):
    data = {
            'keyword': keyword,
            'format': json,
            'page': 1,
            'pagesize': 10
    }
    musiclist = requests.get('http://mobilecdn.kugou.com/api/v3/search/song', params=data, headers= None, cookies = None)
    hashList = json.loads(musiclist.content)
    return hashList['data']['info'][0]['hash']

    # for song in hashList:
    #     hashList.append(song['id'])


# http://m.kugou.com/app/i/getSongInfo.php?hash=2d78a1b92a0bbdabe65513466d69e5bd&cmd=playInfo
def getMusic(key):
    data = {
        'hash': search(key),
        'cmd': 'playInfo'
    }
    musiclist = requests.get('http://m.kugou.com/app/i/getSongInfo.php', params=data, headers= None, cookies = None)
    musicObj = json.loads(musiclist.content)
    return musicObj


# http://www.kugou.com/yy/index.php?r=play/getdata&hash=CB7EE97F4CC11C4EA7A1FA4B516A5D97
def getLyrics(key):
    data = {
        'hash': search(key),
        'r': 'play/getdata'
    }
    lyrics = json.loads(requests.get('http://www.kugou.com/yy/index.php', params=data, headers= None, cookies = None).content)['data']['lyrics']

    lyricsList = lyrics.split('\r\n')
    a = []
    for lyric in lyricsList:
        if '\\' in lyric:
            a.append(lyric[10:].strip['\\'])
        else:
            a.append(lyric[10:])
    return a


@app.route('/music/info', methods=['GET'])
def getMusicInfo():
    musicInfo = getMusic(request.args['keywords'])
    lyricsInfo = getLyrics(request.args['keywords'])
    if 'keywords' in request.args:
        return jsonify(url = musicInfo['url'],title = musicInfo['fileName'],singerName = musicInfo['singerName'],lyrics= lyricsInfo)


@app.route('/api/emotionkey', methods=['POST'])
def createEmotionKey():
    if not request.json or not 'image' in request.json:
        abort(400)
    logging.log(logging.INFO, request.json['image'],'body')
    keywords = getEmotionKey(request.json['image'])
    return keywords


@app.route('/image', methods=['GET', 'POST'])
def upload_file():
    return jsonify(link='http://fs.open.kugou.com/58b8877b417dc9c1179c2f66a304780a/5a216342/G013/M04/19/09/rYYBAFUNoi2AdlG7AC48VTPd088072.mp3',
                   title='Amber Carrington - Sad',artist='Amber Carrington',img='https://i.pinimg.com/736x/dd/21/a5/dd21a5719f50d914faf50c7b01c00a7f--taylor-marie-hill-taylor-hill-face.jpg',lyrics=[
    "SadVoice Performance) - Amber Carrington",
    "Man  it's been a long day",
    "Stuck thinking 'bout it driving on the freeway",
    "Wondering if I really tried everything I could",
    "Not knowing if I should try a little harder",
    "Oh  but i'm scared to tell",
    "That there may not be another one like this",
    "And I confess that i'm only holding on by a thin thin threat",
    "And i'm kicking the curb cause you never heard",
    "The words that you needed so bad",
    "And i'm kicking the dirt cause I never gave you the things that you needed to have",
    "I'm so sad  saaad",
    "Man  it's been a long night",
    "Just sitting here  trying not to look back",
    "Still looking at the road we never drove on",
    "And wondering if the one I chose was the right one",
    "Oh  but i'm scared to tell",
    "That there may not be another one like this",
    "And I confess that i'm only holding on by a thin thin threat",
    "And i'm kicking the curb cause you never heard",
    "The words that you needed so bad",
    "And i'm kicking the dirt cause I never gave you the things that you needed to have",
    "I'm so sad  saaad",
    "And i'm kicking the curb cause you never heard",
    "The words that you needed so bad",
    "And i'm kicking the dirt cause I never gave you the things that you needed to have",
    "And i'm kicking the curb cause you never heard",
    "The words that you needed so bad",
    "And I'm kicking the dirt cause I never gave you",
    "The things that you needed to have",
    "I'm so sad  saaad",
    "I'm so sad",
    ""
  ])
    # if request.method == 'POST':
    #     if 'file' not in request.files:
    #         logging.log(logging.INFO, "No file")
    #         abort(401)
    #         if file.filename == '':
    #             logging.log(logging.INFO, "No selected file")
    #             abort(402)
    #     file = request.files['file']
    #     logging.log(logging.DEBUG, file)
    #     if file:
    #         filename = secure_filename(file.filename)
    #         logging.log(logging.INFO, "os.getcwd() = " + os.getcwd())
    #         directory = os.getcwd()+"/static/"
    #         if not os.path.exists(directory):
    #             os.makedirs(directory)
    #         file.save(os.path.join(directory, "current_image.jpg"))
    #         key = getEmotionKey(directory+"current_image.jpg")
    #         musicInfo = getMusic(key)
    #         lyricsInfo = getLyrics(key)
            # return jsonify(url = musicInfo['url'],title = musicInfo['fileName'],singerName = musicInfo['singerName'],lyrics= lyricsInfo)

            # tasks = []
            # return jsonify({'tasks': tasks})

@app.route('/images', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.log(logging.INFO, "No file")
            abort(401)
            if file.filename == '':
                logging.log(logging.INFO, "No selected file")
                abort(402)
        file = request.files['file']
        logging.log(logging.DEBUG, file)
        if file:
            filename = secure_filename(file.filename)
            logging.log(logging.INFO, "os.getcwd() = " + os.getcwd())
            directory = os.getcwd()+"/static/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(os.path.join(directory, "current_image.jpg"))
            key = getEmotionKey(directory+"current_image.jpg")
            musicInfo = getMusic(key)
            lyricsInfo = getLyrics(key)
            return jsonify(url = musicInfo['url'],title = musicInfo['fileName'],singerName = musicInfo['singerName'],lyrics= lyricsInfo)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}),404)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # print getMusicUrl(u'海阔天空')
    # print getMusic('347231')
    # print getLyrics('sad')
    # print getEmotionKey('https://i.pinimg.com/736x/dd/21/a5/dd21a5719f50d914faf50c7b01c00a7f--taylor-marie-hill-taylor-hill-face.jpg')

    # getEmotionScore()
    app.run(debug=True)
