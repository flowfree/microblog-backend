from .base import * 

SECRET_KEY = 'django-insecure-)pii7wcww@s2kit6i-^r^id!zx=zf++r^r4y$mzh5o7x79e!!p'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [ 
    'sslserver',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    'https://localhost:3000',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
]
