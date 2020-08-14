import requests
import json
from bs4 import BeautifulSoup
import re
from opencc import OpenCC
import pandas as pd
def youtube_get_comment_fin(url):
    MessageCount=0
    video_id=url.split('watch?v=')[1].split('&')[0]
    # 設定要抓幾留言便停止
    comment_limit = 200
    session = requests.Session()
    session.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    # Get Youtube page with initial comments
    first_page_comment_url = 'https://www.youtube.com/all_comments?v=' + video_id
    # 先進入 https://www.youtube.com/all_comments?v=video_id (進入該頁面的目的是拿到session_token)
    response = session.get(first_page_comment_url)
    html = response.text
    # ===找到session_token
    target = 'XSRF_TOKEN'
    start = html.find(target) + len(target) + len('\': \"')  # str.find('target',start index)可找出對應的足碼
    end = html.find('"', start)
    session_token = html[start:end]
    # 設定函式去request
    def ajax_request(session, url, params, data):
        response = session.post(url, params=params, data=data)
        response_dict = json.loads(response.text)
        return response_dict.get('page_token', None), response_dict['html_content']
    # 開始進入留言區
    count = 0
    data_con = pd.DataFrame(columns=['video_id', 'viewer', 'comment', 'time', 'clean_con'])
    # 設定只保留中文、英文、數字（去掉韓語日語德語，也會去掉表情符號等等）
    # reference: https://zhuanlan.zhihu.com/p/84625185
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    ###設定簡體轉繁體方法
    cc = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
    # 進入留言區第一頁時要帶的資料比較不同 data / params (order_menu : True)
    data = {'video_id': video_id, 'session_token': session_token}
    params = {'action_load_comments': 1, 'order_by_time': True, 'filter': video_id, 'order_menu': True}
    # 先設定page_token為真使while作動; 待會跑到最後一頁時，page_token 為空值，因此while停止
    page_token = True
    # 每一頁留言(仿留言往下滑)
    while page_token:
        response_2 = ajax_request(session, 'https://www.youtube.com/comment_ajax', params, data)
        # 留言區的第二頁之後的帶的資料 data / params
        data = {'video_id': video_id, 'session_token': session_token}
        params = {'action_load_comments': 1, 'order_by_time': True, 'filter': video_id}
        # response_2[0] 為 page_token
        # response_2[1] 為 回傳訊息的留言內容區
        page_token = response_2[0]
        data['page_token'] = page_token
        res = BeautifulSoup(response_2[1], 'html.parser')
        # 使用標籤取出每一頁的留言
        coent = res.select('div.comment-text-content')  # 留言
        user_name = res.select('a.user-name')  # 留言者
        coent_time = res.select('span.time')  # 留言時間
        # 開始記錄留言進dataframe (data_con)
        for i in range(len(coent_time)):
            content = cc.convert(''.join(coent[i].text.strip().split('\n')))
            # 整理出乾淨的留言
            clean_data = rule.sub(' ', str(content))
            if len(rule.sub('', str(clean_data))) < 1:
                clean_content = 'NAN'
            else:
                clean_content = clean_data.strip(' ')
            # 加入pa.dataframe時順便將簡體轉成繁體
            data_con = data_con.append(
                {'video_id': video_id, 'viewer': cc.convert(user_name[i].text.strip()), 'comment': content,
                 'time': coent_time[i].text.strip(), 'clean_con': clean_content}, ignore_index=True)
            # 計算幾篇留言
            count += 1
            if count > comment_limit:
                page_token = None
                break
        print('page_token: {}'.format(page_token))
    return data_con