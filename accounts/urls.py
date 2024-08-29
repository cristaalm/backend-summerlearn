from django.urls import include, path
from .views import status_list, rol_list
from .authenticate import register_user, login_user
from accounts import views, authenticate


urlpatterns = [

    path('users/', views.user_list),  
    path('status/', views.status_list), 
    path('rol/', views.rol_list),
    path('register/', authenticate.register_user),
    path('login/', authenticate.login_user),
]


