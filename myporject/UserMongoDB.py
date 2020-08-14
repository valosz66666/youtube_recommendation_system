import requests
from bs4 import BeautifulSoup
import json
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import pandas as pd
import os
import time
import shutil
import csv
import pymongo as pm
import datetime
from pprint import pprint
import socket
class MongoOperator:
    def __init__(self, host, port, db_name, default_collection): #mongo port:27017
        self.client = pm.MongoClient(host=host, port=port)        #建立資料庫連線
        self.db = self.client.get_database(db_name)        #選擇相應的資料庫名稱
        self.collection = self.db.get_collection(default_collection)        #設定預設的集合
    def insert(self, item, collection_name =None): #增加資料 目錄,檔名
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            collection.insert(item)
        else:
            self.collection.insert(item)
    def find(self, expression =None, collection_name=None): #查詢 expression:條件 collection_name:檔名
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            if expression == None:
                return collection.find()
            else:
                return collection.find(expression)
        else:
            if expression == None:
                return self.collection.find()
            else:
                return self.collection.find(expression)
    def get_collection(self, collection_name=None):#查詢集合內容物
        if collection_name == None:
            return self.collection
        else:
            return self.get_collection(collection_name)
def Els(ip,key,WebDict):
    FeatFlow= {"FeatFlow":{
        "MainFollow": None,
        "ChannelAvgLook": None,
        "FeatFollow": None,
        "FeatAvgLook": None,
        "FeatTable": None
    }}
    AiTitle = {"AiTitle":{
        "MakeTitle": None,
        "MakeArticle":None
    }}
    MessageEmotion= {"MessageEmotion":{
        "VideoUrl": None
    }}
    YoutubeFlow = {"YoutubeFlow":{
        "ChannelVideoLookMedian": None,
        "ChannelVideoLookAvg": None,
        "ChannelFollow": None,
        "OneHourFlow": None
    }}
    YoutubeReport = {"YoutubeReport":{
        "ChannelClass": None,
        "Channel_Avg_Look": None
    }}
    NewsWordCloud= {"NewsWordCloud":{
        "SelectDate":None,
        "KeyWord":None,
        "BarDateCount":None
    }
    }
    if key=="NewsWordCloud":
        NewsWordCloud={"NewsWordCloud":WebDict}
    if key=="FeatFlow":
        FeatFlow = {"FeatFlow":WebDict}
    if key=="AiTitle":
        AiTitle = {"AiTitle":WebDict}
    if key=="MessageEmotion":
        MessageEmotion = {"MessageEmotion":WebDict}
    if key=="YoutubeReport":
        YoutubeReport = {"YoutubeReport":WebDict}
    if key=="YoutubeFlow":
        YoutubeFlow={"YoutubeFlow":WebDict}
    ElsDict={}
    Date = '%Y-%m-%d'
    Time='%H:%M:%S'
    ElsDict["ip"]=ip
    ElsDict["Date"]=datetime.datetime.now().strftime(Date)
    ElsDict["Time"]=datetime.datetime.now().strftime(Time)
    ElsDict.update(NewsWordCloud)
    ElsDict.update(FeatFlow)
    ElsDict.update(AiTitle)
    ElsDict.update(MessageEmotion)
    ElsDict.update(YoutubeFlow)
    ElsDict.update(YoutubeReport)
    return ElsDict
def SaveMongoDB(Data):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_port =s.getsockname()[0]
    db = MongoOperator(ip_port, 27017, 'UserRecord', 'UserRecord')  # IP DBNAME Table
    s.close()
    db.insert(Data)