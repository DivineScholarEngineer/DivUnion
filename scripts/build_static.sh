#!/bin/bash
# Build static site for deployment on platforms like Netlify.
# This script collects static files and uses django-distill to output
# static HTML versions of the site into the ``distill_build`` directory.

set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Generating static build via django-distill..."
python manage.py distill-local --force

echo "Static build completed. Files are available in the distill_build/ directory."
