"""Settings for the test suite, which shouldn't need a real secret key."""
import os

os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-secret-key-long-enough-for-hs256-signing")

from budget.settings import *  # noqa: E402,F401,F403
