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
from django.urls import path,include,re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from challenge import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from challenge.compile_run_processor import candidate_compile_run

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('auth/',include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')), #REST FRAMEWORK
    path('',views.candidate_compile_run,name='compile_run_api'),
    path('home/',views.home, name="home"),
    path('loggedout/',auth_views.LogoutView.as_view(template_name="home.html"),name="logout"),
    path('management/',include('challenge.urls')),
    path('candidate_details/<uuid:challenge_id>', views.candidate_details,name="candidate_details"), 
    path('sample_lang_codes/', views.sample_language_codes,name="sample_language_codes"), 
    path('challenge_instructions/<uuid:challenge_id>/<uuid:candidate_id>', views.instructions,name="instructions"),
    path('test/<uuid:challenge_id>/<uuid:candidate_id>/test_page/running', views.test_page,name="test_page"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
