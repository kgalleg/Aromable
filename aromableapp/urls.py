from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = "aromableapp"

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^home$', home, name='home'),
    url(r'^categories$', category_list, name='categories'),




    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout_user, name='logout'),
]