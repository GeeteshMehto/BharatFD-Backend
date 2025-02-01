#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 BUILD START"

# Install SQLite dependencies
apk update && apk add --no-cache sqlite-libs

# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Run Django migrations
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput

echo "✅ BUILD END"
