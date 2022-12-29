from django.urls import path 
from . import views 


urlpatterns = [
	path('', views.home_page, name='home'),
	path('post-create/', views.post_create, name='post_create'),
]