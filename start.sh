#!/usr/bin/env bash
set -o errexit

if [ -z "${SECRET_KEY:-}" ] && [ -z "${DJANGO_SECRET_KEY:-}" ]; then
  export SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
fi

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}"
