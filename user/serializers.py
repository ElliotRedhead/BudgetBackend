from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JwtTokenObtainPairSerializer,
)


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        # Add custom claim
        token["user_id"] = user.id
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """Create a user and respond with a JWT pair, so they're logged in at once."""

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "access", "refresh")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create the user through the manager so the password is hashed."""
        return get_user_model().objects.create_user(**validated_data)

    def to_representation(self, instance):
        """Return the new user's email with a fresh access and refresh token."""
        refresh = TokenObtainPairSerializer.get_token(instance)
        return {
            "email": instance.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
