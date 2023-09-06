"""infoMingle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MAIN.views import news_list
from filter_search.views import category_news_list
# from use_info.views import use_info
# from filter_search.views import category_news_list
from MAIN.views import word_cloud
from MAIN import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news_list, name='main_page'),
    path('category_news/', category_news_list, name='category_news_page'),
    path('word_cloud/', views.word_cloud, name='word_cloud'),  # URL 패턴 수정
]