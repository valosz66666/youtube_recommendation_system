from django.urls import path,re_path
from . import views
from django.conf.urls import url  #導入url套件

app_name='myapp'

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    url('^ajax/ajax_index_Img/$', views.ajax_index_Img, name="ajax_index_Img"),
    path('YoutubeReport/', views.YoutubeReport, name="YoutubeReport"),
    url(r'^ajax/ajax_youtube_report_img/$', views.ajax_YoutubeReport_Img, name="ajax_youtube_report_img"),
    url(r'^ajax/ajax_Two_YoutubeReport_Img/$', views.ajax_Two_YoutubeReport_Img, name="ajax_Two_YoutubeReport_Img"),
    path('YoutubeFlow/', views.YoutubeFlow, name="YoutubeFlow"),
    path('NewWordCloud/', views.NewWordCloud, name="NewWordCloud"),
    re_path(r'^ajax/ajax_NewWordCloud_Img/$', views.ajax_NewWordCloud_Img, name="ajax_NewWordCloud_Img"),
    re_path(r'^ajax/Json_Ajax/$', views.Json_Ajax, name="Json_Ajax"),
    path('FeatFlow/', views.FeatFlow, name="FeatFlow"),
    re_path(r'^ajax/featflow/$', views.ajax_featflow, name="ajax_featflow"),
    path('MessageEmotion/', views.MessageEmotion, name="MessageEmotion"),
    re_path(r'^ajax/ajax_MessageEmotion/$', views.ajax_MessageEmotion, name="ajax_MessageEmotion"),
    path('AiToTitle/', views.AiToTitle, name="AiToTitle"),
    re_path('^ajax/ajax_AiToTitle_Img/$', views.ajax_AiToTitle_Img, name="ajax_AiToTitle_Img"),
    re_path('^ajax/AjaxTitle/$', views.AjaxTitle, name="AjaxTitle"),
    path('MessageEmotion/', views.MessageEmotion, name="MessageEmotion"),
    re_path(r'^ajax/ajax_MessageEmotion/$', views.ajax_MessageEmotion, name="ajax_MessageEmotion"),
]
