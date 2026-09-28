from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=get_user_model().objects.all(), lookup="iexact"
                    )
                ]
            },
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        """Apply AUTH_PASSWORD_VALIDATORS, including similarity to the email."""
        candidate_user = get_user_model()(email=attrs["email"])
        try:
            validate_password(attrs["password"], user=candidate_user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error
        return attrs

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
