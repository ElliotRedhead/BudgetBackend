FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UV_PROJECT_ENVIRONMENT=/venv \
	UV_PYTHON_DOWNLOADS=never \
	PATH="/venv/bin:$PATH"
WORKDIR /backend
COPY pyproject.toml uv.lock /backend/
RUN uv sync --locked
COPY . /backend/
