from bs4 import BeautifulSoup
import requests
import json
def youtube_videoinfo_json(url):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

    # get web response
    html = requests.get(url, headers=headers)
    response = BeautifulSoup(html.text, 'html.parser')

    a = response.select('script')  # 目標json在window["ytInitialData"]在當中，在a的倒數第3個
    data_str = str(a[-4]).split("""window["ytInitialData"] = """)[1].split("}};")[
                   0] + "}}"  # window["ytInitialData"] = {"responseContext":{... 的字串檔

    # 處理成完整的json格是再做json.loads
    data_dict = json.loads(data_str)

    # print(data_dict)
    # ===開始取資料
    # 該影片相關資訊
    set_a = data_dict['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
    print(set_a)

    # 該影片的頻道相關資訊
    set_b = data_dict['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']
    video_title = set_a['title']['runs'][0]['text']
    video_view_count = set_a['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
    video_post_date = set_a['dateText']['simpleText']
    video_like_count = set_a['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText']['simpleText']
    video_dislike_count = set_a['videoActions']['menuRenderer']['topLevelButtons'][1]['toggleButtonRenderer']['defaultText']['simpleText']
    channel_of_video = set_b['title']['runs'][0]['text']
    channel_id_of_video = set_b['title']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']
    video_title=''.join(video_title.split(' '))
    VideoStatistics=[]
    VideoStatistics.append('影片標題:'+video_title)
    VideoStatistics.append('\n'+video_view_count)
    VideoStatistics.append('發佈日期:'+video_post_date)
    VideoStatistics.append('按讚數:'+video_like_count)
    VideoStatistics.append('倒讚數:'+video_dislike_count)
    VideoStatistics.append('頻道名稱:'+channel_of_video)
    VideoStatistics.append('頻道ID:'+channel_id_of_video)
    return VideoStatistics