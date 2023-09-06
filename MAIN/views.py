from django.shortcuts import render
import urllib.request
import json
import os
import sys
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(BASE_DIR, 'static/fonts/NanumGothicBold.otf')

# from numpy.random._examples.cython.extending import mask
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.template import loader

# texts_with_links = [
#     {"text": "Python", "link": "https://www.python.org/"},
#     {"text": "Django", "link": "https://www.djangoproject.com/"},
# ]

# def wordcloud_view(request):
#     context = {'texts_with_links': texts_with_links}
#     return render(request, 'main.html', context)

def news_list(request):
    apiKey = "233a4af135d54c7d8367531181458156"
    url = "https://newsapi.org/v2/top-headlines?country=kr&apiKey=" + apiKey
    url_request = urllib.request.Request(url)
    response = urllib.request.urlopen(url_request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        decode = response_body.decode('utf-8')
        results = json.loads(decode)
        items = results['articles']
        total = results["totalResults"]
        context = {'items': items, 'total': total}
        return render(request, 'main.html', context)


def word_cloud(request):
    apiKey = "233a4af135d54c7d8367531181458156"
    url = "https://newsapi.org/v2/top-headlines?country=kr&apiKey=" + apiKey
    url_request = urllib.request.Request(url)
    response = urllib.request.urlopen(url_request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        decode = response_body.decode('utf-8')
        results = json.loads(decode)
        items = results['articles']
        wordcloudsource = ""
        for item in items:
            wordcloudsource = wordcloudsource + str(item["title"]) + str(item["description"])
        okt = Okt()
        line = []
        line = okt.pos(wordcloudsource)
        n_adj = []
        # 명사 또는 형용사인 단어만 n_adj에 넣어주기
        for word, tag in line:
            if tag in ['Noun', 'Adjective']:
                n_adj.append(word)
        # 명사 또는 형용사인 단어 및 2글자 이상인 단어 선택 시
        n_adj = [word for word, tag in line if tag in ['Noun', 'Adjective'] and len(word) > 1]
        print(n_adj)
        # 제외할 단어 추가
        stop_words = "아니었네요. 있어서 끝 있는 든 유사시"  # 추가할 때 띄어쓰기로 추가해주기
        stop_words = set(stop_words.split(' '))
        # 불용어를 제외한 단어만 남기기
        n_adj = [word for word in n_adj if not word in stop_words]
        # 가장 많이 나온 단어 100개 저장
        counts = Counter(n_adj)
        tags = counts.most_common(100)
        font='static/fonts/NanumGothicBold.otf'
        ###WordCloud(워드크라우드) 만들기###
        # word_cloud = WordCloud(font_path=font, background_color='black',max_font_size=400, mask=mask,colormap='prism').generate_from_frequencies(dict(tags))
        word_cloud = WordCloud(font_path=FONT_PATH, background_color='white', max_font_size=200, colormap='cool').generate_from_frequencies(dict(tags))
        # word_cloud = WordCloud(font_path="C://Users//ksh15//flutter//bin//cache//artifacts//material_fonts//roboto-black.ttf", background_color='white', max_font_size=200,
        #                        colormap='cool').generate_from_frequencies(dict(tags))
        #
        # word_cloud = WordCloud(background_color='black', max_font_size=200, colormap='prism').generate_from_frequencies(dict(tags))

        plt.figure(figsize=(8, 8))
        plt.imshow(word_cloud)
        plt.axis('off')

        # 이미지를 바로 출력
        response = HttpResponse(content_type="image/png")
        word_cloud.to_image().save(response, "PNG")
        return response
