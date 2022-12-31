from django.urls import path 
from . import views


urlpatterns = [
	path('comment-create/<int:post_pk>/', views.comment_create, name='comment_create'),
	path('comment/<int:pk>/update/', views.comment_update, name='comment_update'),
	path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]