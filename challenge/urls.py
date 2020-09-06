from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from challenge import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('create_test', views.create_test, name="create_test")
]
