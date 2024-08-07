from django.urls import path
from django.conf.urls.static import static
from .views import BusinessDetailView, LoginView, RegistrationView, LogoutView, SessionView, BusinessView
from django.conf import settings

app_name = 'api'
urlpatterns = [
    path('account/register', RegistrationView.as_view()),
    path('account/login', LoginView.as_view()),
    path('account/logout', LogoutView.as_view()),
    path('account/session', SessionView.as_view()),
    path('business', BusinessView.as_view()),
    path('business/<int:id>', view=BusinessDetailView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
