web: gunicorn warehouse_management.wsgi --log-file -
worker: celery -A maroulakoswarehouse worker
beat: celery -A maroulakoswarehouse beat -S django