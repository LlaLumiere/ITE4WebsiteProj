from django.urls import path
from . import views
from .views import SaveChatView, get_saved_chat

urlpatterns = [
    path('', views.base, name='base'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.user_home, name='home'), 
    path('logout/', views.logout_user, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('ask/', views.ask, name='ask'),
    path('save_chat/', SaveChatView.as_view(), name='save_chat'),
    path('get_saved_chat/', views.get_saved_chat, name='get_saved_chat'),

]