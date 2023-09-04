from django.shortcuts import render
import urllib.request
import json

def category_news_list(request):
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
        return render(request, 'filterMain.html', context)