from django.urls import path
from django.conf.urls.static import static
from .views import LoginView, RegistrationView, LogoutView, SessionView
from django.conf import settings

app_name = 'api'
urlpatterns = [
    path('account/register', RegistrationView.as_view()), 
    path('account/login', LoginView.as_view()),   
    path('account/logout', LogoutView.as_view()),   
    path('account/session', SessionView.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
