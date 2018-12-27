import os
import environ


root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(
    DEBUG=(bool, False),
) # set default values and casting
environ.Env.read_env() # reading .env_example file

HEROKU = env('HEROKU')
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'USER': env('DB_USER'),
        'NAME': env('DB_NAME'),
        'PASSWORD': env('DB_PASS'),
        'TEST': {
            'NAME': 'test_flying_bear_bot',
        },
    },
}


if HEROKU:
    STATIC_URL = '/static/'

    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']
    # Static asset configuration
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_ROOT = 'staticfiles'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
)