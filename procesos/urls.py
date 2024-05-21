from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]