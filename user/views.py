from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import RegisterSerializer, TokenObtainPairSerializer


class RegisterView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
