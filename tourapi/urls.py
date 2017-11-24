from django.conf.urls import url
from tourapi import views

urlpatterns = [
	
	#TOURISTS

	url(r'tourists/register/', views.api_register_tourist, name='api_register_tourist'),
    url(r'tourists/all/', views.api_get_tourists, name='api_tourists'),
    url(r'tourists/(?P<tourist>\d+)/', views.api_get_single_tourist, name='api_single_tourist'),
    url(r'tourists/(?P<tourist>)\d+/tourisms/', views.get_tourist_tourisms, name='api_tourist_tourisms'),
    url(r'tourists/tourism/add/', views.api_register_tourism, name='api_add_tourism'),
    url(r'tourists/tourism/all/', views.api_get_tourisms, name='api_tourisms'),
    url(r'tourists/tourism/(?P<tourism>\d+)/', views.api_get_single_tourism, name='api_single_tourism'),

    #SP

    url(r'sp/register/', views.api_sp_register, name='api_sp_register'),
    url(r'sp/all/', views.api_get_sp_all, name='api_sp_all'),
    url(r'sp/(?P<sp>\d+)/', views.api_get_single_sp, name='api_sp')
]
