from django.urls import path
from .views import User_APIView, User_APIView_Detail

app_name = 'api'
urlpatterns = [
    path('user', User_APIView.as_view()), 
    path('user/<int:pk>/', User_APIView_Detail.as_view()),   
]