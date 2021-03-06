#coding=utf-8
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from confluent_kafka import Producer
from bs4 import BeautifulSoup
from confluent_kafka import Consumer, KafkaException, KafkaError
import requests
import json
from opencc import OpenCC
import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import lxml.html
import re
import urllib.parse
from opencc import OpenCC
import pandas as pd
import numpy as np
import csv
import jieba
import pymysql
from random import randint
pwd=os.path.dirname(__file__)
#使用網路上簡體的中文詞庫: https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/dict.txt.big
#記得將簡體的中文詞庫轉成繁體(可以使用opencc套件轉成繁體)，轉完的檔案為dict.txt.big_new.txt
def is_alphabet(keyword):
    return all(ord(c) < 128 for c in keyword)
def WordCloud_Color(pd_csv,video_id):
    pwd = os.path.dirname(__file__)
    jieba.set_dictionary(pwd + '/dict.txt.big_new.txt')
    # 再加入我們從維基百科建立的自訂字典:self_define_dict.txt，可以將專有名詞成功斷開-->蔡英文、韓國瑜
    # 這個自定義字典存檔時記得使用utf-8的編碼存檔
    jieba.load_userdict(pwd + '/self_define_dict.txt')
    # 讀入stopwords.txt並做成 stopwords 字典
    stopwords = {}
    with open(pwd + r'/test_dict_stop.txt', 'r', encoding='UTF-8') as file:
        for st_word in file.readlines():
            st_word = st_word.strip()  # data.strip()為去除前後空白
            stopwords[st_word] = 1
    FilePath = pwd
    ImgPath = pwd + r'/static/images'
    wd_dict = {}
    # 新聞總檔案
    # 有些中文字python預設為unicode無法編譯，例如游錫堃的堃，使用encoding ='utf-8-sig'
    for j, content in enumerate(pd_csv['clean_con']):
        # 這個是將udn的內容中有該段文字給替換成空白
        content = content.replace(
            '''domready(function() {if ( !countDownStatus ) getCountdown();if ( !highChartsStatus ) getHighcharts();});domready(function() {var channelId = 2;var actArea = "poll_at_story_0_v773";var actCode = "v773";var actTemplate = "bar2";var elemDiv = document.createElement('div');elemDiv.id = actArea;elemDiv.className ='vote_body area';var scr = document.getElementById(actArea+'_script');scr.parentNode.insertBefore(elemDiv, scr);$.getScript('/funcap/actIndex.jsp?actCode=' + actCode + '&channelId=' + channelId , function() {actTemplate = eval('objAct_' + actCode + '.d1.actTemplate');$.ajaxSetup({ cache: true });$.getScript('/func/js/' + actTemplate + '_min.js?2019122401', function() {$.ajaxSetup({ cache: false });piepkg();loadTemplateJs(actTemplate);eval(actTemplate + 'view("' + '#' + actArea + '");')})});});''',
            '')
        content = content.strip('').strip('\n').strip('')  # 去除文章前後的空白與斷行
        seg_con_list = jieba.cut(content)
        # 拿stopwords來清理jieba處理完的字串
        for wd in seg_con_list:
            wd = wd.strip('')
            if is_alphabet(wd) != True:
                if stopwords.get(wd) == None and len(wd) > 1:
                    if wd_dict.get(wd) == None:  # 開始計算字詞的數量，未出現的單字存入字典
                        wd_dict[wd] = 1
                    else:  # 開始計算字詞的數量，出現過的單字字典數加1
                        wd_dict[wd] += 1
            # 每篇文章做完再進到下一行

    print("影片ID:{}".format(video_id))
    # === deal with similarity_dict ===
    fw = open(pwd + r'/similarity_dict.txt', 'r', encoding='utf-8-sig')
    sy_list = []
    while True:
        line = fw.readline()
        b = line.strip('\n').strip(' ')
        a = b.split(',')
        sy_list.append(a)
        if not line:
            break
    fw.close()
    sy_list.pop()  # 將最後一個空串列丟出
    ncount = 0
    for n, syn in enumerate(sy_list):
        for i in range(len(syn)):
            ncount += wd_dict.get(syn[i], 0)
            if wd_dict.get(syn[i]) != None:
                del wd_dict[syn[i]]
        wd_dict[syn[0]] = ncount
        ncount = 0
    print(wd_dict)
    # del wd_dict['不拘']
    # ===== 生成文字雲 ======
    def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None,
                          random_state=None):
        h = randint(0, 240)
        # s = int(100.0 * 255.0 / 255.0)
        s = randint(70, 100)
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)

    ###http://csscoke.com/2015/01/01/rgb-hsl-hex/ HSL調色###
    # font設定成微軟正黑體，這邊我是直接抓我windows中的字體檔案，將該檔案放在程式的同一個工作目錄下即可
    font = pwd + '/NotoSansCJKtc-Black.otf'
    # wordcloud = WordCloud(background_color='white',font_path=font,scale=5)
    wordcloud = WordCloud(background_color='white', font_path=font, max_font_size=50, min_font_size=10, scale=10,
                          max_words=500)
    # 文字雲使用頻率，輸入值為字詞數的字典 (wd_dict)
    my_wordcloud = wordcloud.generate_from_frequencies(frequencies=wd_dict)
    # 畫出文字雲
    my_wordcloud.recolor(color_func=random_color_func)
    plt.axis("off")
    wordcloud.to_file(ImgPath + '/{}.png'.format(video_id))


