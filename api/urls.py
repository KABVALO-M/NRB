from django.urls import path
from . import views 

urlpatterns = [
    path('citizens/', views.get_citizens, name='get_citizens'),  # API endpoint for citizens
]
