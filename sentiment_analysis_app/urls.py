
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('power_bi_visual1/', views.power_bi_visual1, name='power_bi_visual1'),
    path('power_bi_visual2/', views.power_bi_visual2, name='power_bi_visual2'),
    path('analyze_sentiment/', views.analyze_sentiment, name='analyze_sentiment'), 
    path('healthz/', views.health_check, name='healthz'),
]
