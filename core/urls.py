from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect_view, name='home'),  
    path('dashboard/', views.dashboard_view, name='dashboard'),  
    path('login/', views.login_view, name='login'),  
    path('users/', views.users_view, name='users'),  
    path('users/add/', views.add_user_view, name='add_user'),  
    path('citizens/', views.citizens_view, name='citizens'),  
    path('deceased-citizens/', views.deceased_citizens_view, name='deceased_citizens'),  
    path('logout/', views.logout_view, name='logout'),  
    
    path('citizens/add/', views.add_citizen_view, name='add_citizen'),
    path('users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),  
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),  
    
    path('citizens/edit/<int:citizen_id>/', views.edit_citizen_view, name='edit_citizen'),  
    path('citizens/delete/<int:citizen_id>/', views.delete_citizen_view, name='delete_citizen'),  
    
    path('deceased/add/', views.add_deceased_citizen_view, name='add_deceased_citizen'),
    path('deceased/edit/<int:id>/', views.edit_deceased_citizen_view, name='edit_deceased_citizen'),
    path('deceased/delete/<int:id>/', views.delete_deceased_citizen_view, name='delete_deceased_citizen'),
]
