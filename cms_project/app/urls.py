from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user_registration'),
    path('login', UserLoginView.as_view(), name='user_login'),  
    path('getcontent', GetAllContentView.as_view(), name='getcontent'),  
    path('create', CreateContentView.as_view(), name='create'),  
    path('delete', DeleteContentView.as_view(), name='delete_content'),

]
