wsgi_app = "DB_library.wsgi:application"
bind = "127.0.0.1:8000"
reload = True
accesslog = errorlog = "/arcade/django/logs/gunicorn.log"
capture_output = True
#daemon = True
