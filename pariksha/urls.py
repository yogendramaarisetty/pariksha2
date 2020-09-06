"""pariksha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from challenge import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
     path('auth/',include('django.contrib.auth.urls')),
    path('',views.home, name="home"),
    path('loggedout/',auth_views.LogoutView.as_view(template_name="home.html"),name="logout"),
    path('management/',include('challenge.urls')),
    path('candidate_details/<uuid:challenge_id>', views.candidate_details,name="candidate_details"), 
    path('sample_lang_codes/', views.sample_language_codes,name="sample_language_codes"), 
    path('challenge_instructions/<uuid:challenge_id>/<uuid:candidate_id>', views.instructions,name="instructions"),
    path('test/<uuid:challenge_id>/<uuid:candidate_id>/test_page/running', views.test_page,name="test_page"),
url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
