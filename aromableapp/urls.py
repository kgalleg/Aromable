from django.conf.urls import url
from .views import *

app_name = "aromableapp"

urlpatterns = [
    url(r'^$', category_list, name='home'),
    url(r'^categories$', category_list, name='categories'),
]