# coding:utf-8
import os

Img_Size = '''
    width="100" height="150"
'''
pwd = os.path.dirname(__file__)
ImgPath = pwd + r'/static/images'
os.chdir(ImgPath)  # 換工作路徑
file_list = os.listdir(ImgPath)  # 這個資料夾內所有的檔案名稱
PngName = []
for i in file_list[::-1]:
    PngName.append(i)


def ajax_index_Img(request):
    word = {}
    i = random.sample(PngName, 1)
    Greap = '''<img class ="card1-img1-top1" src="\static\images\{}" alt="" {}>'''.format(i[0], Img_Size)
    word[i[0]] = Greap
    return JsonResponse(word)


def index(request):
    return render_to_response('index.html', locals())


import os

pwd = os.path.dirname(__file__)
Img_Size = '''
    width="900" height="600"
'''


def UserClassPandas():
    FilePath = pwd + r'/流量分類.csv'
    ClassPd = pd.read_csv(FilePath)
    return ClassPd


def EnglishToChinese(string):
    if string == '教育類':
        return 'Education'
    if string == '娛樂類':
        return 'Entertainment'
    if string == '遊戲類':
        return 'Game'
    else:
        return 'Movie'


def Get_Avg_Look(string):
    if string == '20萬以上':
        return 'TOP1'
    if string == '5萬至20萬':
        return 'TOP2'
    if string == '2萬至5萬':
        return 'TOP3'
    if string == '2萬以下':
        return 'TOP4'


from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def ajax_YoutubeReport_Img(request):
    if request.GET.get("channel_class") != '':
        User_Select_Class = request.GET.get("channel_class")  # 取得分類
        category = EnglishToChinese(User_Select_Class)
        ImgPathFile = pwd + r'/static/images/cat_image/{}'.format(category)
        os.chdir(ImgPathFile)  # 換工作路徑
        file_list = os.listdir(ImgPathFile)  # 這個資料夾內所有的檔案名稱
        PngName = []
        for i in file_list:
            if 'png' in i:
                PngName.append(i)
        cont = []
        for n, name in enumerate(PngName):
            category_name = ["影片發佈時間點分析", "影片發佈流量高峰期", '主要發片時間點與流量高峰期相對關係', '影片發佈流量高峰期']
            if 'hist' in name:
                GraphClass = 'bar'
            elif 'line' in name:
                GraphClass = 'area'
            GraphCount = '{}'.format(i)
            ImgStrPath = '/static/images/cat_image/{}/{}'.format(category, name)
            cont.append({"GraphClass": GraphClass, "User_Select_Class": User_Select_Class, "GraphCount": GraphCount,
                         "name": name[:-4], "ImgStrPath": ImgStrPath, "Img_Size": Img_Size})
        DataPd = UserClassPandas()
        Channel_Avg_Look_Pandas = DataPd['均觀看數']
        for n, Channel_Avg_Look_Interval in enumerate(Channel_Avg_Look_Pandas):
            cont[n]["Channel_Avg_Look_Interval"] = Channel_Avg_Look_Interval
            cont[n]["Channel_Class_Avg_Look_Interval"] = User_Select_Class + Channel_Avg_Look_Interval

        return JsonResponse(cont, safe=False)


@api_view(["GET", "POST"])
def ajax_Two_YoutubeReport_Img(request):
    if request.GET.get("Channel_Avg_Look") != '':
        User_Select_Class = request.GET.get("Channel_Avg_Look")
        if "電影與動畫" in User_Select_Class:
            category = EnglishToChinese(User_Select_Class[:5])
            TOP_Count = Get_Avg_Look(User_Select_Class[5:])
        else:
            category = EnglishToChinese(User_Select_Class[:3])
            TOP_Count = Get_Avg_Look(User_Select_Class[3:])

        word = {}
        ImgPath = pwd + r"/static/images/cat_image/{}/{}_{}".format(category, category, TOP_Count)
        os.chdir(ImgPath)  # 換工作路徑
        file_list = os.listdir(ImgPath)  # 這個資料夾內所有的檔案名稱
        PngName = []
        for i in file_list:
            if 'png' in i:
                PngName.append(i)
        GraphData = ''
        cont = []
        for n, name in enumerate(PngName):
            name = str(name)
            if 'hist' in name:
                GraphClass = 'bar'
            elif 'line' in name:
                GraphClass = 'area'
            category_name = ["影片發佈時間點分析", "影片發佈流量高峰期", '主要發片時間點與流量高峰期相對關係', '影片發佈流量高峰期']
            GraphCount = '{}'.format(i)
            ValueName = 'stream{}'.format(i)
            ImgStrPath = '/static/images/cat_image/{}/{}_{}/{}'.format(category, category, TOP_Count, name)
            GraphData += '''             <div class="col-xl-6">
                                                        <div class="card mb-4">
                                                            <div class="card-header"><i class="fas fa-chart-{} mr-1"></i>{}</div>
                                                            <div class="card-img-top" id='Statistics_{}' name='Statistics_{}'  alt="">
                                                                 '<img value='{}' src='{}' {} />'</div>
                                                            <div class="card-body"><canvas id="my{}raph" width="100%" height="40"></canvas></div>
                                                        </div>
                                                    </div>
                                                    '''.format(GraphClass, User_Select_Class + category_name[n],
                                                               GraphCount, GraphCount, ValueName,
                                                               ImgStrPath, Img_Size, i)
        word[User_Select_Class] = GraphData
        return JsonResponse(word)


def YoutubeReport(request):
    DataPd = UserClassPandas()  # 取得建呈提供的欄位
    Channel_Class_Pandas = DataPd['類別']  # 用在網頁上下拉式選單
    Channel_Class_Pandas.dropna(axis=0, how='any', inplace=True)  # 刪除下拉式選單的空值
    return render(request, 'YoutubeReport.html', locals())  # 只要有這行就可以讀取html檔顯示網頁


from django.shortcuts import render
import pandas as pd
import joblib


# sys.path.append(pwd+"../kafka_producer.py")
# import kafka_producer

def prediction(MainFollow, VideoAvgLike, FeatFollow, FeatAvgLike):
    loaded_DTmodel = joblib.load(pwd + r"/DT_rg_model.sav")
    at = [[MainFollow, VideoAvgLike, FeatFollow, FeatAvgLike]]
    DT = loaded_DTmodel.predict(at)
    return round(float(DT), 0)


def YoutubeFlow(request):
    if 'VideoAvgLike' in request.GET and request.GET['VideoAvgLike'] != '':
        VideoAvgLike = float(request.GET["VideoAvgLike"])
        ChannelFollow = float(request.GET["ChannelFollow"])
        OneHourFlow = float(request.GET["OneHourFlow"])
        ChannelMedian = float(request.GET["ChannelMedian"])
        DTPredict = prediction(ChannelMedian, VideoAvgLike, ChannelFollow, OneHourFlow)
        return render_to_response('YoutubeFlow.html', locals())
    else:
        return render_to_response('YoutubeFlow.html', locals())


import json

import os

import random

from django.shortcuts import render_to_response
from django.http import JsonResponse

from .plot_keyword_diagram import plot_keyword_djagram

pwd = os.path.dirname(__file__)
Img_Size = '''
    width="1000" height="858"    
'''


@api_view(["GET", "POST"])
def ajax_NewWordCloud_Img(request):
    User_Select_Class = request.GET.get("date")
    request.session["Last"] = User_Select_Class
    word = {}
    GraphData = ''
    i = '1'

    PatternName = str(User_Select_Class) + '文字雲'
    GraphCount = '{}'.format(i)
    ValueName = 'stream{}'.format(i)
    ImgStrPath = '/static/images/{}.png'.format(User_Select_Class)
    GraphData += '''             

                                                <div class="card-header"><i class=""></i>{}</div>
                                                <div class="card-img-top" id='Statistics_{}' name='Statistics_{}'  alt="" >
                                                     '<img value='{}' src='{}' {} />'</div>
                                                <div class="card-body"><canvas id="my{}raph" width="100%" height="40%"></canvas></div>

                                        '''.format(PatternName, GraphCount, GraphCount, ValueName,
                                                   ImgStrPath, Img_Size, i)
    word[User_Select_Class] = GraphData
    print(word)
    return JsonResponse(word)


def NewWordCloud(request, JsonDictName=None):
    FilePath = pwd
    JsonPath = pwd
    os.chdir(JsonPath + r'/keyword')  # 換工作路徑
    file_list = os.listdir(JsonPath)  # 這個資料夾內所有的檔案名稱
    JsonName = []
    global Page
    Page = 1
    for i in file_list[::-1]:
        if 'json' in i:
            if 'wordcount_2020.json' not in i:
                JsonName.append(i)
    JsonPath = random.sample(JsonName, 1)[0]
    OpenJson = open(pwd + r'/{}'.format(JsonPath), 'r', encoding="utf-8-sig")
    OpenJson = json.load(OpenJson)
    JsonPath = JsonPath[:-5]
    global AjaxDict
    AjaxDict = OpenJson
    JsonKey = OpenJson.keys()
    JsonDict = {}
    for n, i in enumerate(JsonKey):
        JsonDict[i] = OpenJson[i]
        if n == 9:
            break
    ImgPath = pwd + r'/static/images'
    os.chdir(ImgPath)  # 換工作路徑
    file_list = os.listdir(ImgPath)  # 這個資料夾內所有的檔案名稱
    PngName = []
    for i in file_list[::-1]:
        if 'png' in i:
            PngName.append(i[:-4])

    if "Last" in request.session:  # 檢查指定的session是否存在
        meowdate = request.session["Last"]
        meow = "\static\images\\" + str(request.session["Last"]) + ".png"
    try:
        if request.GET["KeyWord"] != "":
            KeyWord = request.GET["KeyWord"]
            InputDay = request.GET["InputDay"]
            plot_keyword_djagram(KeyWord, int(InputDay))
            plot_path = "\static\plt\{}{}.png".format(KeyWord, InputDay)
            return render_to_response('NewWordCloud.html', locals())
    except Exception as e:
        print(e)
        return render_to_response('NewWordCloud.html', locals())


@api_view(["GET", "POST"])
def Json_Ajax(request):
    word = {}
    JsonDict = AjaxDict
    JsonKey = []
    global Page
    k = Page
    for i in JsonDict.keys():
        JsonKey.append(i)
    for i in JsonKey[k * 10:k * 10 + 10]:
        word[i] = JsonDict[i]
    Page += 1
    return JsonResponse(word)


import os
from django.shortcuts import render_to_response
from django.http import JsonResponse
import joblib
import sys

pwd = os.path.dirname(__file__)


def prediction(MainFollow, VideoAvgLike, FeatFollow, FeatAvgLike):
    loaded_model = joblib.load(pwd + r"/lnrg_model.sav")
    loaded_RFmodel = joblib.load(pwd + r"/RF_rg_model.sav")
    at = [[MainFollow, VideoAvgLike, FeatFollow, FeatAvgLike]]
    Ln = loaded_model.predict(at)
    Rf = loaded_RFmodel.predict(at)
    return int(Ln), round(float(Rf), 2)


def FeatFlow(request):
    # LnFeatPredict,RfFeatPredict=prediction(546546,978978,97878,798798)
    Class_list = ["娛樂類", "人物與部落客", "教育類", "電影與動畫", "遊戲類"]
    if 'VideoAvgLike' in request.GET and request.GET['VideoAvgLike'] != '':
        a = float(1.0)
        VideoAvgLike = float(request.GET["ChannelVideoFollow"])
        Channel_Follow = float(request.GET["VideoAvgLike"])
        FeatFollow = float(request.GET["FeatFollow"])
        FeatVideoAvgLike = float(request.GET["FeatVideoAvgLike"])
        LnFeatPredict, RfFeatPredict = prediction(VideoAvgLike, Channel_Follow, FeatFollow, FeatVideoAvgLike)
        return render_to_response('FeatFlow.html', locals())
    return render_to_response('FeatFlow.html', locals())


@api_view(["GET", "POST"])
def ajax_featflow(request):
    if request.GET.get("Feat_Class") != '':
        UserClass = request.GET.get("Feat_Class")
        request.session["FeatTable"] = UserClass
        ImagePath = "/static/images/{}.jpg".format(UserClass)
        Grapt = ''' 
                                    <div class="card mb-4">
                                        <div class="card-header"><i class="fas fa-chart-bar mr-1"></i>{}一年內合作影片數量</div>
                                            <img class="card-img-top"   src='{}' alt="">
                                        <div class="card-body"><canvas id="myAreaChart" width="100%" height="40%"></canvas></div>
                                    </div>

        '''.format(UserClass, ImagePath)
        word = {}
        word[UserClass] = Grapt
        return JsonResponse(word)


import os
from django.shortcuts import render_to_response
from django.http import JsonResponse
import joblib
import sys

pwd = os.path.dirname(__file__)


def prediction(MainFollow, VideoAvgLike, FeatFollow, FeatAvgLike):
    loaded_RFmodel = joblib.load(pwd + r"/RF_rg_model.sav")
    at = [[MainFollow, VideoAvgLike, FeatFollow, FeatAvgLike]]
    Rf = loaded_RFmodel.predict(at)
    return round(float(Rf), 2)


def FeatFlow(request):
    # LnFeatPredict,RfFeatPredict=prediction(546546,978978,97878,798798)
    Class_list = ["娛樂類", "人物與部落客", "教育類", "電影與動畫", "遊戲類"]
    if 'VideoAvgLike' in request.GET and request.GET['VideoAvgLike'] != '':
        a = float(1.0)
        VideoAvgLike = float(request.GET["ChannelVideoFollow"])
        Channel_Follow = float(request.GET["VideoAvgLike"])
        FeatFollow = float(request.GET["FeatFollow"])
        FeatVideoAvgLike = float(request.GET["FeatVideoAvgLike"])
        RfFeatPredict = prediction(VideoAvgLike, Channel_Follow, FeatFollow, FeatVideoAvgLike)
        return render_to_response('FeatFlow.html', locals())
    return render_to_response('FeatFlow.html', locals())


@api_view(["GET", "POST"])
def ajax_featflow(request):
    if request.GET.get("Feat_Class") != '':
        UserClass = request.GET.get("Feat_Class")
        request.session["FeatTable"] = UserClass
        ImagePath = "/static/images/{}.jpg".format(UserClass)
        Grapt = ''' 
                                    <div class="card mb-4">
                                        <div class="card-header"><i class="fas fa-chart-bar mr-1"></i>{}一年內合作影片數量</div>
                                            <img class="card-img-top"   src='{}' alt="">
                                        <div class="card-body"><canvas id="myAreaChart" width="100%" height="40%"></canvas></div>
                                    </div>

        '''.format(UserClass, ImagePath)
        word = {}
        word[UserClass] = Grapt
        return JsonResponse(word)


from django.shortcuts import render_to_response
from django.http import JsonResponse
import os

pwd = os.path.dirname(__file__)
from .Youtube_data import youtube_videoinfo_json
from .While_SVC_Model import SVC_model
from .YoutubeMessage import youtube_get_comment_fin
from .wordcloud_color import WordCloud_Color


@api_view(["GET", "POST"])
def ajax_MessageEmotion(request):
    word = {}
    ImgStrPath = '''  
                                        <div class="col-xl-6">
                                            <div class="card mb-4">
                                                <div class="card-header"><i class="fas fa-chart-cloud mr-1"></i>爬蟲準備中</div>
                                                <div class="card-img-top" id='Statistics_TOW' name='Statistics_TWO'  alt="">
                                                     '<img value='adfsdfas' src='/static/images/VKSPIDER.gif'  width="1021" height="900" /></div>
                                                <div class="card-body"><canvas id="myAraph" width="100%" height="40%"></canvas></div>
                                            </div>
                                        </div>
                                        '''

    word['VideoUrl'] = ImgStrPath
    return JsonResponse(word)
    # return render_to_response('MessageEmotion.html',locals())
    # data_con.to_csv(CsvPath+'\{}.csv'.format(video_id), index=0, encoding='utf-8-sig')


def MessageEmotion(request):
    if 'UserGetVideoUrl' in request.GET and request.GET['UserGetVideoUrl'] != '':
        VideoUrl = request.GET["UserGetVideoUrl"]

        HtmlCodeList = youtube_videoinfo_json(VideoUrl)  # 把程式丟進爬蟲抓影片標題 發佈日期 等等資訊
        video_id = VideoUrl.split('watch?v=')[1].split('&')[0]  # 取得Video ID
        csv_pd = youtube_get_comment_fin(VideoUrl)
        WordCloud_Color(csv_pd, video_id)
        SVC_model(csv_pd, video_id)  # 把網址丟進爬蟲程式
        Pie_Name = 'sentiment_pie_{}.png'.format(video_id)
        Video_Image = '/static/images/{}.png'.format(video_id)
        Pie_Image = '/static/images/{}'.format(Pie_Name)
        return render_to_response('MessageEmotion.html', locals())

    else:
        return render_to_response('MessageEmotion.html', locals())


@api_view(["GET", "POST"])
def ajax_AiToTitle_Img(request):
    word = {}
    ImgStrPath = '''  
                            <div class="card mb-4">
                                <div class="card-header" ><i class="fas fa-chart-cloud mr-1"></i>腳本生成中</div>
                                        <div >
                                        <img class="adfsdfas" id='Statistics_One' name='Statistics_One'  src='/static/images/VKTitle.gif' alt="" width="1100" height="1100">
                                        </div>
                                <div class="card-body"><canvas id="myAreaChart" width="100%" height="40"></canvas></div>
                            </div>

                                        '''
    word['VideoUrl'] = ImgStrPath
    return JsonResponse(word)


def AjaxTitle(request):
    word = {}

    ImgStrPath = '''

                            <div class="card mb-4">
                                <div class="card-header" ><i class="fas fa-chart-cloud mr-1"></i>標題生成中</div>
                                        <div >
                                        <img class="adfsdfas" id='Statistics_One' name='Statistics_One'  src='/static/images/AiTitle.gif' alt="" width="1100" height="1100">
                                        </div>
                                <div class="card-body"><canvas id="myAreaChart" width="100%" height="40"></canvas></div>
                            </div>

                                        '''

    word['VideoUrl'] = ImgStrPath
    return JsonResponse(word)


from .summary_candidate_fin import summary_candidate_fin
from .generate_own_script_test1 import GPT2Article


def AiToTitle(request):
    if "Article" in request.GET:
        Article = request.GET["Article"]
        MakeArticle = GPT2Article(Article)
        return render(request, 'AiToTitle.html', locals())
    elif "UserArticle" in request.GET:
        Article = request.GET["UserArticle"]
        Title_list = summary_candidate_fin(Article)
        return render(request, 'AiToTitle.html', locals())
    return render(request, 'AiToTitle.html', locals())
