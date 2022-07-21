FROM python:3.10-alpine
ENV POETRY_VERSION=1.1.12 \
	POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY pyproject.toml poetry.lock .env /backend/
RUN pip install "poetry==$POETRY_VERSION"
COPY . /backend/
RUN poetry config virtualenvs.create false
RUN poetry install
