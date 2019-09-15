from django.conf.urls import url
from senders import views

urlpatterns = [
    url(r'^register/account', views.RegisterSenderView.as_view(), name='register'),
    url(r'^register/success/', views.RegisterSenderSuccessView.as_view(), name='register_success'),
    url(r'^register/failed/', views.RegisterSenderFailedView.as_view(), name='register_failed'),
    url(r'^register/access_token/', views.SenderAccessToken.as_view(), name='register_access_token'),
    # url(r'^register/access_token/', views.RegisterSenderView.access_token_callback, name='register_access_token'),
]
