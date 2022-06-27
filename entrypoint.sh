python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn config.wsgi:application --bind 127.0.0.1:8000
