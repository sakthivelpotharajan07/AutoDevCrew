Target Language: Python

DEBUG = True
SECRET_KEY = 'mysecretkey'
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
LOGIN_REDIRECT_URL = '/home'
LOGOUT_REDIRECT_URL = '/login'
LOGIN_URL = '/login'