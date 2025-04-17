from django.urls import path,include
from .views import RegistrationView,LoginApiView,LogoutApiView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
]
