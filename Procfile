release: ./release-tasks.sh
web: gunicorn app.core:app -w 4 --preload
worker: celery -A app.celery_builder.celery worker
