#!/bin/bash
set -e

export PYTHONPATH=/app
export DB_CONNECTION="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@/${POSTGRES_DB}?host=/var/run/postgresql"

cd /app
/opt/venv/bin/python -m src.load_database