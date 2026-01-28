import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from user.models import User


@pytest.mark.django_db
class TestRegister:
    """Assert registration creates a user and returns a usable JWT pair."""

    def setup_method(self):
        """Instantiate APIClient and registration payload."""
        self.client = APIClient()
        self.url = "/user/register/"
        self.payload = {"email": "new@user.com", "password": "P4ssw0rd123!"}

    def test_register_returns_tokens(self):
        """Return access and refresh tokens for the newly created user."""
        response = self.client.post(self.url, self.payload)

        assert response.status_code == 201
        user = User.objects.get(email="new@user.com")
        assert AccessToken(response.data["access"])["user_id"] == user.id
        assert response.data["refresh"]

    def test_register_does_not_return_password(self):
        """Never echo the submitted password in the response."""
        response = self.client.post(self.url, self.payload)

        assert response.status_code == 201
        assert "password" not in response.data
        assert response.data["email"] == "new@user.com"

    def test_registered_access_token_authenticates(self):
        """Access token from registration can reach protected endpoints."""
        response = self.client.post(self.url, self.payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {response.data['access']}")

        assert self.client.get("/expenses/").status_code == 200
