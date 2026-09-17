from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/new/', views.create_group, name='create_group'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('group/<int:pk>/edit/', views.edit_group, name='edit_group'),
    path('group/<int:pk>/join/', views.join_group, name='join_group'),
    path('group/<int:pk>/leave/', views.leave_group, name='leave_group'),
    path('group/<int:pk>/requests/<int:membership_id>/', views.respond_to_request, name='respond_to_request'),
]
