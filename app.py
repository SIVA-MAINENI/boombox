import urllib.request
import wave
import webbrowser
from datetime import datetime, date
from random import random
import pyaudio
# import houndify

# import pymongo as pymongo
import requests
# import urllib3
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

# app = Flask(__name__)

# connectionString = 'mongodb://doverhackathon2022-database:uYtbE1mzGJYZPXBJgEsXuU7Fi2N9jEJ26KF4H5oW2GTKKJyWivpPYABwenEeMQcr3jrRMQe2Z2FKXjizcPjZsA==@doverhackathon2022-database.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@doverhackathon2022-database@'
# client = pymongo.MongoClient(connectionString)
# db = client.get_database('RewardSystem')
# activityByUser = db.get_collection('ActivityByUser')
# ad_db = client.get_database('AdSystem')
# product_collect = ad_db.get_collection('ProfileMappings')
# cars_collect = ad_db.get_collection('VehicleMappings')


# @app.route('/monitor')
# def monitor():  # put application's code here
#     return jsonify(status="success")


# @app.route('/updateActivity', methods=["POST"])
# def updateActivity():
#     send = request.json

#     updateDate = str(datetime.now())
#     active_user = activityByUser.find_one({"token": send["token"], "storeID": send["storeID"]})

#     #print(active_user["updateDate"])

#     if active_user is None:
#         rewardPoints = (send["gallonCount"] % 10) * 5
#         if rewardPoints < 1:
#             rewardPoints = 0
#         activityByUser.insert_one({"token": send["token"], "storeID": send["storeID"],
#                                    "gallonCount": send["gallonCount"], "updateDate": str(updateDate),
#                                    "Rewards": rewardPoints})
#         active_user = activityByUser.find_one({"token": send["token"], "storeID": send["storeID"]})

#     else:
#         if (datetime.now() - datetime.strptime(active_user['updateDate'], "%Y-%m-%d %H:%M:%S.%f")).days <= 30:
#             rewardPoints = (active_user['gallonCount'] % 10) * 5 + active_user['Rewards']
#         else:
#             rewardPoints = (active_user['gallonCount'] % 10) * 5

#             #  Update the User account with rewards
#         activityByUser.update_one({"token": send["token"], "storeID": send["storeID"]},
#                                   {
#                                       '$set': {'Rewards': rewardPoints,
#                                                'updateDate': str(datetime.now())}
#                                   })

#     products = product_collect.find({'kids': send['kids'], 'weather': send['weather'],
#                                      'QuantityAvailable': {'$gte': 0},
#                                      'Rewards': {'$lte': rewardPoints}})

#     product_recommend = []
#     for document in products:
#         product_recommend.append(document['ProductName'])

#     product_recommend = list(set(product_recommend))[:2]
#     cars_ad = cars_collect.find_one({'CarType': send['car_type'].capitalize()})['Profiling']

#     return (jsonify(token=active_user["token"], storeID=active_user["storeID"],
#                     Rewards=rewardPoints, cars_ad=cars_ad, product_recommend=product_recommend))


# @app.route('/weather')
# def weather():
#     return jsonify(status=random.randint(0, 1))


# @app.route('/identifyMusic')
def identifyMusic():
    data = {
        'api_token': 'ec7774e96686cda94583d6d7d282d06c',
        'return': 'spotify',
    }

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    try:
        while True:
            data1 = stream.read(1024)
            frames.append(data1)
    except KeyboardInterrupt:
        pass
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sound_file = wave.open("myrecording.mp3", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()
    files = {
        'file': open('myrecording.mp3', 'rb'),
    }
    data = {
    'api_token': 'ec7774e96686cda94583d6d7d282d06c',
    'return': 'spotify',
    }
    #files = request.data
    result = requests.post('https://api.audd.io/', data=data, files=files)
    print("heello",result.text)
    result = result.json()

    hdr = {'Accept': 'text/html', 'Connection': 'keep-alive', 'Accept-Encoding': 'none',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)', 'Connection': 'keep-alive'}
    link = result["result"]["song_link"]
    print(link)
    conn = urllib.request.Request(url=link, headers=hdr)
    html = urllib.request.urlopen(conn).read()
    # html = conn.read()
    soup = BeautifulSoup(html)
    links = soup.find_all('a')


    finalLink=""
    for tag in links:
        link = tag.get('href', None)
        if link is not None and "https://youtube.com" in link:
            finalLink=link

    webbrowser.open(finalLink)

    return jsonify(link=finalLink)


if __name__ == '__main__':
    identifyMusic()
     
