import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testuser.gmail.com'
EMAIL_HOST_PASSWORD = 'testpassword'
EMAIL_PORT = 587

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}