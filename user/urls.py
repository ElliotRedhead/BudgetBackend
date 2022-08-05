from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import EmailTokenObtainPairView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
