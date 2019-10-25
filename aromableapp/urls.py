from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "aromableapp"

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('categories/', category_list, name='categories'),



    path('recipes/', recipe_list, name='recipes'),

    path('recipe/form', recipe_form, name='recipe_form'),

    path('recipes/<int:recipe_id>/', recipe_details, name='recipe'),
    path('recipes/<int:recipe_id>/form', recipe_edit_form, name='recipe_edit_form'),




    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout_user, name='logout'),
]