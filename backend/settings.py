from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "gin",
    'drf_spectacular',
    #"inscription",
    "stages",
    "accounts",
    "partenaires",
    "realisations",
    "services",
    "equipe",
    'corsheaders',
    'contact',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # DOIT ÊTRE EN PREMIER
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'backend.middleware.CSRFExemptAPIMiddleware',  # Notre middleware personnalisé
]

# Configuration CORS sécurisée et flexible
DEBUG_MODE = config('DEBUG', default=True, cast=bool)

# Pour le développement, on peut être plus permissif
if DEBUG_MODE:
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",  
        "http://127.0.0.1:3000", 
    ]

# Ajouter des domaines via variable d'environnement
FRONTEND_URLS = config('FRONTEND_URLS', default='').split(',')
if FRONTEND_URLS and FRONTEND_URLS != ['']:
    CORS_ALLOWED_ORIGINS.extend([url.strip() for url in FRONTEND_URLS if url.strip()])

# Si CORS_ALLOW_ALL_ORIGINS est True en production, désactiver les credentials pour la sécurité
if CORS_ALLOW_ALL_ORIGINS and not DEBUG_MODE:
    CORS_ALLOW_CREDENTIALS = False
    print("⚠️ WARNING: CORS_ALLOW_ALL_ORIGINS=True en production - CORS_ALLOW_CREDENTIALS désactivé pour la sécurité")
elif not DEBUG_MODE:
    CORS_ALLOW_CREDENTIALS = True

# Headers CORS autorisés
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
]

# Méthodes HTTP autorisées
CORS_ALLOWED_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Permettre l'envoi de cookies et headers d'authentification
CORS_ALLOW_CREDENTIALS = True

# Configuration pour les requêtes preflight
CORS_PREFLIGHT_MAX_AGE = 86400


ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # C'est ça qui manque

# Si ce n’est pas déjà là :
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email Configuration
# Pour Gmail, utilisez un mot de passe d'application : https://support.google.com/accounts/answer/185833
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=config('EMAIL_HOST_USER', default='noreply@gin.com'))
CONTACT_EMAIL = config('CONTACT_EMAIL', default=config('EMAIL_HOST_USER', default='contact@gin.com'))

# Email timeout settings
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=30, cast=int)

# SSL configuration for email
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None

# Custom SSL context for problematic certificates
import ssl

# Configuration SSL plus permissive pour les serveurs avec certificats problématiques
EMAIL_SSL_VERIFY = config('EMAIL_SSL_VERIFY', default=True, cast=bool)

if not EMAIL_SSL_VERIFY:
    # Création d'un contexte SSL personnalisé pour ignorer les erreurs de certificat
    import ssl
    from functools import wraps
    
    def create_unverified_context():
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    
    # Monkey patch pour Django
    try:
        import smtplib
        original_starttls = smtplib.SMTP.starttls
        
        def patched_starttls(self, keyfile=None, certfile=None, context=None):
            if context is None:
                context = create_unverified_context()
            return original_starttls(self, keyfile, certfile, context)
        
        smtplib.SMTP.starttls = patched_starttls
    except Exception as e:
        print(f"Erreur lors du patch SSL: {e}")

# En mode développement, vous pouvez utiliser le backend console pour tester
if DEBUG and config('USE_CONSOLE_EMAIL', default=False, cast=bool):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'GIN API',
    'DESCRIPTION': "Documentation de l'API backend de GIN",
    'VERSION': '1.0.0',
    'CONTACT': {'email': 'maxaraye18@gmail.com'},
    'LICENSE': {'name': 'BSD License'},
    'SERVE_INCLUDE_SCHEMA': False,
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
