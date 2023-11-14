from django import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import MyTokenObtainPairView, RegisterView, getUser, updateUser, LogoutView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('user/', getUser, name='user'),
    path('user/update/', updateUser, name='user_update'),
]
