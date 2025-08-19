from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'), # Home page
    path('home_kor/', views.home_kor, name='home_kor'), # Home page in Korean
    path('home_ind/', views.home_ind, name='home_ind'), # Home page in Indonesian

    path('order/', views.order, name='order'),# How to order Jamu page
    path('order_kor/', views.order_kor, name='order_kor'),
    path('order_ind/', views.order_ind, name='order_ind'),

    path('JamubyAI/', views.JamubyAI, name='Jamu by AI'), # Jamu by AI page
    path('JamubyAI_kor/', views.JamubyAI_kor, name='Jamu by AI_kor'),
    path('JamubyAI_ind/', views.JamubyAI_ind, name='Jamu by AI_ind'),

    path('CreateYourBlend/', views.CreateYourBlend, name='Create Your Blend'),
    path('CreateYourBlend_kor/', views.CreateYourBlend_kor, name='Create Your Blend_kor'),
    path('CreateYourBlend_ind/', views.CreateYourBlend_ind, name='Create Your Blend_ind'),

    path('info/', views.info, name='info'), # Description of Jamu page
    path('info_kor/', views.info_kor, name='info_kor'),
    path('info_ind/', views.info_ind, name='info_ind'),

    path('chatbot/', views.chatbot, name='chatbot'), # Chatbot page
    path('chatbot_kor/', views.chatbot_kor, name='chatbot_kor'),
    path('chatbot_ind/', views.chatbot_ind, name='chatbot_ind'),

    path('ourstory/', views.ourstory, name='our story'), # Our story page
    path('ourstory_kor/', views.ourstory_kor, name='our story_kor'),
    path('ourstory_ind/', views.ourstory_ind, name='our story_ind'),

    # API endpoints
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/order-status/', views.order_status_api, name='order_status_api'),

    path('HowToOrder/', views.HowToOrder, name='How to Order'), # How to Order page
    path('HowToOrder_kor/', views.HowToOrder_kor, name='How to Order_kor'), # How to Order page in Korean
    path('HowToOrder_ind/', views.HowToOrder_ind, name='How to Order_ind'), # How to Order page in Indonesian
]