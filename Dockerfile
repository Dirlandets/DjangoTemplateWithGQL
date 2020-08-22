FROM python:3.8-slim as base

LABEL maintainer="leonid@shestera.com"
LABEL securitytxt="https://openapi.finex.plus/.well-known/security.txt"

ARG BUILD_DEPS="build-essential libcairo2-dev libpango1.0-dev libffi-dev git"

ARG DJANGO_ENV

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIPENV_DOTENV_LOCATION=.env

# hadolint ignore=DL3008, DL3013
RUN set -ex && \
    groupadd -r app && \
    useradd -r -s /bin/false -g app app && \
    apt-get update && \
    apt-get install -y --no-install-recommends $BUILD_DEPS && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

# hadolint ignore=SC2046,DL3013
RUN set -ex && \
    pip install pipenv==2018.11.26 && \
    pipenv install --deploy --system --ignore-pipfile $([ "$DJANGO_ENV" = "production" ] || echo "--dev")

WORKDIR /app

COPY . ./app

FROM base

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--user", "app", "--workers", "4", "app.wsgi:application", "--log-file", "-"]