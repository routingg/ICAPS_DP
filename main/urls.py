from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'), # Home page
    path('home_kor/', views.home_kor, name='home_kor'), # Home page in Korean
    path('home_indonesian/', views.home_indonesian, name='home_indonesian'), # Home page in Indonesian
    path('home_eng/', views.home_eng, name='home_eng'), # Home page in English

    path('order/', views.order, name='order'),# How to order Jamu page

    path('JamubyAI/', views.JamubyAI, name='Jamu by AI'), # Jamu by AI page
    path('CreateYourBlend/', views.CreateYourBlend, name='Create Your Blend'), # Create Your Blend page

    path('info/', views.info, name='info'), # Description of Jamu page

    path('chatbot/', views.chatbot, name='chatbot'), # Chatbot page
    path('ourstory', views.ourstory, name='our story'), # Candidate 3 page
    
    # API endpoints
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/order-status/', views.order_status_api, name='order_status_api'),

    
]