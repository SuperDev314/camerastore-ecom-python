from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'register$', views.register, name='register'),
    url(r'create', views.register, name='create_account'),
    url(r'login', views.login, name='login'),
    url(r'logout$', views.logout, name='logout'),
]
