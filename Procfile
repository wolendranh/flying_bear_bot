release: python manage.py migrate --noinput
web: newrelic-admin run-program gunicorn flying_bear_bot.wsgi --log-file -