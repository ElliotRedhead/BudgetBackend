import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from user.models import User


@pytest.mark.django_db
class TestLogin:
    """Assert login and refresh exchange credentials for JWTs."""

    def setup_method(self):
        """Create a user with a known password and instantiate APIClient."""
        self.client = APIClient()
        self.password = "P4ssw0rd123!"
        self.user = User.objects.create_user(
            email="user@user.com", password=self.password
        )

    def test_login_returns_tokens_for_user(self):
        """Valid credentials return an access token for that user."""
        response = self.client.post(
            "/user/login/", {"email": "user@user.com", "password": self.password}
        )

        assert response.status_code == 200
        assert AccessToken(response.data["access"])["user_id"] == self.user.id
        assert response.data["refresh"]

    def test_login_ignores_email_case(self):
        """The email matches however it's cased at login."""
        response = self.client.post(
            "/user/login/", {"email": "User@USER.com", "password": self.password}
        )

        assert response.status_code == 200
        assert AccessToken(response.data["access"])["user_id"] == self.user.id

    def test_login_rejects_unknown_email(self):
        """An unknown email is rejected like a wrong password."""
        response = self.client.post(
            "/user/login/", {"email": "nobody@user.com", "password": self.password}
        )

        assert response.status_code == 401

    def test_login_rejects_wrong_password(self):
        """A wrong password is rejected without tokens."""
        response = self.client.post(
            "/user/login/", {"email": "user@user.com", "password": "wrong"}
        )

        assert response.status_code == 401
        assert "access" not in response.data

    def test_login_rejects_inactive_user(self):
        """A deactivated user can't log in."""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            "/user/login/", {"email": "user@user.com", "password": self.password}
        )

        assert response.status_code == 401

    def test_refresh_returns_new_access_token(self):
        """A refresh token can be exchanged for a new access token."""
        login_response = self.client.post(
            "/user/login/", {"email": "user@user.com", "password": self.password}
        )
        response = self.client.post(
            "/user/refresh/", {"refresh": login_response.data["refresh"]}
        )

        assert response.status_code == 200
        assert AccessToken(response.data["access"])["user_id"] == self.user.id

    def test_refresh_token_cannot_be_reused(self):
        """Refreshing rotates the refresh token and revokes the old one."""
        login_response = self.client.post(
            "/user/login/", {"email": "user@user.com", "password": self.password}
        )
        old_refresh = login_response.data["refresh"]

        first_refresh = self.client.post("/user/refresh/", {"refresh": old_refresh})
        reused_refresh = self.client.post("/user/refresh/", {"refresh": old_refresh})

        assert first_refresh.status_code == 200
        assert first_refresh.data["refresh"] != old_refresh
        assert reused_refresh.status_code == 401

    def test_logout_revokes_refresh_token(self):
        """After logout the refresh token can't be used again."""
        login_response = self.client.post(
            "/user/login/", {"email": "user@user.com", "password": self.password}
        )
        refresh = login_response.data["refresh"]

        logout_response = self.client.post("/user/logout/", {"refresh": refresh})
        refresh_response = self.client.post("/user/refresh/", {"refresh": refresh})

        assert logout_response.status_code == 200
        assert refresh_response.status_code == 401

    def test_refresh_rejects_invalid_token(self):
        """A malformed refresh token is rejected."""
        response = self.client.post("/user/refresh/", {"refresh": "not-a-token"})

        assert response.status_code == 401
