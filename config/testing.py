from .default import *

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME',''),
        'USER': os.environ.get('DB_USER',''),
        'PASSWORD': os.environ.get('DB_PASSWORD',''),
        'HOST': os.environ.get('DB_HOST',''),
        'PORT': 5432,
    }