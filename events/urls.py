from django.conf.urls import url
from events import views

urlpatterns = [
    url(r'^access_token', views.EventAccessToken.as_view()),
]
