from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'), # Home page
    path('issues/', views.issues, name='issues'), # Health issues page
    path('order/', views.order, name='order'),# How to order Jamu page
    path('info/', views.info, name='info'), # Description of Jamu page
    path('waiting/', views.waiting, name='waiting'), # Waiting page
    path('complete/', views.complete, name='complete'), # complete page
    path('chatbot/', views.chatbot, name='chatbot'), # Chatbot page
    
    # API endpoints
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/order-status/', views.order_status_api, name='order_status_api'),


    # candidates for front
    path('candidate1/', views.candidate1, name='candidate1'), # Candidate 1 page
    path('candidate2/', views.candidate2, name='candidate2'), # Candidate 2 page
    path('candidate3/', views.candidate3, name='candidate3'), # Candidate 3 page
    path('candidate4/', views.candidate4, name='candidate4'), # Candidate 4 page
    

    path('test/', views.test, name='test'), # Test page


    path('order1/', views.order1, name='order1'), # Order 1 page
    path('order2/', views.order2, name='order2'), # Order 2 page
    path('order3/', views.order3, name='order3'), # Order 3 page
    path('order4/', views.order4, name='order4'), # Order 4

    path('home_kor/', views.home_kor, name='home_kor'), # Home page in Korean
    path('home_indonesian/', views.home_indonesian, name='home_indonesian'), # Home page in Indonesian
    path('home_eng/', views.home_eng, name='home_eng'), # Home page in English

    path('jamu_info/', views.jamu_info, name='jamu_info'), # Jamu info page
    
]