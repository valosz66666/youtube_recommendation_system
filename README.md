********爬取YouTube資料進行分析及推薦的系統******
前言
由於Youtube的影響力日漸提高，傳統的電視節目已經要被YouTube取代了，就連總統候選人、市長候選人都要上各大網紅頻道增加知名度，因此爬取YouTube資料做分析，希望能夠提供有用的資訊給使用者。

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%B8%BD%E7%B5%B1.PNG)

首頁
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/index.PNG)

一.爬蟲資料來源
1.Youtube
2.TVBS
3.LTN
4.UDN
5.ETToday
6.NEXTTV

二.六項服務
1.熱門題材
爬取每天的新聞，將每天的新聞數乘上一個係數，讓每天的字詞權重相當，如今天有600篇新聞，明天有900篇新聞，乘上平均數，讓每天的熱門詞基準變成750篇新聞。
再從這些資料中做成文字雲及Json檔供使用者查詢趨勢圖。

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%86%B1%E9%96%80%E9%A1%8C%E6%9D%90.PNG)

執行結果

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%86%B1%E9%96%80%E9%A1%8C%E6%9D%90%E7%B5%90%E6%9E%9C.PNG)

2.影片留言分析
目的
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%95%99%E8%A8%80%E5%88%86%E6%9E%90.PNG)
爬取不同影片的留言，並自行貼標籤，正向或負向，資料約8000筆，將每則留言斷詞以後轉換成稀疏矩陣做成特徵值訓練，並且比較多種演算法以及python其他的文字探勘套件的準確度。
此為python第三方套件SnowNLP的訓練結果，該套件有內建的訓練集，因此做比較。
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E6%AF%94%E8%BC%83%E6%BA%96%E7%A2%BA%E5%BA%A6.PNG)
![image]https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/snownlp.PNG)
可以看出只使用自己貼標籤的資料，準確度最高。
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E6%AF%94%E8%BC%83%E6%BA%96%E7%A2%BA%E5%BA%A6.PNG)
自行使用四種演算法做訓練，並跟SnowNLP比較
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E8%87%AA%E8%A1%8C%E8%A8%93%E7%B7%B4%E7%B5%90%E6%9E%9C.PNG)
此為網站畫面
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%95%99%E8%A8%80%E5%88%86%E6%9E%90%E7%B6%B2%E7%AB%99.PNG)
爬取的目標網站
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%9B%AE%E6%A8%99%E7%B6%B2%E7%AB%99.PNG)
現場爬蟲使用訓練好的model做情感分析
![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E7%95%99%E8%A8%80%E5%88%86%E6%9E%90%E7%B5%90%E6%9E%9C.PNG)

3.標題腳本生成器
標題生成器
使用擷取式的方式 原理

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E6%A8%99%E9%A1%8C%E7%94%9F%E6%88%90%E5%99%A8.PNG)

對新聞做實測

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E6%A8%99%E9%A1%8C%E7%94%9F%E6%88%90%E5%99%A8%E5%AF%A6%E6%B8%AC.PNG)

對影片內容作實測

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E6%A8%99%E9%A1%8C%E7%94%9F%E6%88%90%E5%99%A8%E5%BD%B1%E7%89%87%E5%AF%A6%E6%B8%AC.PNG)

腳本生成器
使用GPT2

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E8%85%B3%E6%9C%AC%E7%94%9F%E6%88%90%E5%99%A8.PNG)

訓練資料來源

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E8%85%B3%E6%9C%AC%E7%94%9F%E6%88%90%E5%99%A8%E5%AF%A6%E6%B8%AC.PNG)

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E8%85%B3%E6%9C%AC%E8%A8%93%E7%B7%B4%E8%B3%87%E6%96%99.PNG)

腳本生成實測

![image](https://github.com/valosz66666/youtube_recommendation_system/blob/master/images/%E8%85%B3%E6%9C%AC%E7%94%9F%E6%88%90%E5%99%A8%E7%B5%90%E6%9E%9C.PNG)

4.流量分析圖表

5.影片流量預測

6.合作流量預測
