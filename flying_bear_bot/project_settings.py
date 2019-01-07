import os
import environ


root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(
    DEBUG=(bool, False),
    HEROKU=(bool, False),
    BOT_WEBHOOK=(str, '')
) # set default values and casting
environ.Env.read_env() # reading .env_example file

HEROKU = env('HEROKU')

ALLOWED_HOSTS = ['*']

if HEROKU:
    STATIC_URL = '/static/'

    import dj_database_url
    # Parse database configuration from $DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config()
    }

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Static asset configuration
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = 'staticfiles'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
)
else:
    DATABASES = {
        'default': {
            'ENGINE': env('DB_ENGINE'),
            #'USER': env('DB_USER'),
            'NAME': env('DB_NAME'),
            #'PASSWORD': env('DB_PASS'),
            'TEST': {
                'NAME': 'test_flying_bear_bot',
            },
        },
    }
    TELEGRAM_BOT = [{
        'token': env('TOKEN'),
        'register': env('BOT_REGISTER_METHOD'),
        'webhook': env('BOT_WEBHOOK')
    }]