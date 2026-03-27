from pathlib import Path
from datetime import timedelta

# BASE_DIR points to the 'backend/' folder that contains manage.py.
# All file paths in settings are built relative to this.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY signs cookies, sessions, and CSRF tokens.
# In production this must come from an environment variable, never be hardcoded.
SECRET_KEY = 'django-insecure--_7*1@1biucra-9)k(yp6wlpvd!6=d9x&!z9(5#*0ed*4b6!%s'

# DEBUG=True enables detailed error pages. Must be False in production.
DEBUG = True

# Only these hostnames can serve the app. Empty = localhost only in dev.
ALLOWED_HOSTS = []


# --- Installed Apps ---
# Django requires every app to be listed here so it can find models,
# admin registrations, and management commands.
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',       # the /admin/ UI
    'django.contrib.auth',        # user model + password hashing
    'django.contrib.contenttypes',# generic relations framework
    'django.contrib.sessions',    # server-side sessions (used by admin)
    'django.contrib.messages',    # one-time flash messages
    'django.contrib.staticfiles', # serving CSS/JS/images

    # Third-party
    'rest_framework',                        # Django REST Framework — turns Django into an API server
    'rest_framework_simplejwt',              # JWT auth — issues and validates access/refresh tokens
    'rest_framework_simplejwt.token_blacklist',  # enables logout by blacklisting refresh tokens
    'corsheaders',                           # CORS — allows the React dev server to call this API

    # Our apps
    'accounts',                   # custom user model + auth endpoints
    'products',                   # product catalog and categories
    'orders',                     # cart and order management
]

# CorsMiddleware MUST come before CommonMiddleware so CORS headers
# are added before Django processes the request further.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',          # <-- CORS, must be high up
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# --- Database ---
# We use PostgreSQL. psycopg2-binary is the driver that connects Django to Postgres.
# These credentials must match what you set up locally (or via docker).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopnest',
        'USER': 'prarthanashiwakoti',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# --- Custom User Model ---
# We tell Django to use our own User model (defined in accounts/models.py).
# This is a best practice: doing it from the start avoids a painful migration later
# if you ever need to add fields (like phone number) to the user.
AUTH_USER_MODEL = 'accounts.User'


# --- Django REST Framework ---
# DEFAULT_AUTHENTICATION_CLASSES: how DRF identifies who is making a request.
# JWTAuthentication reads the Authorization: Bearer <token> header.
# DEFAULT_PERMISSION_CLASSES: by default, all endpoints require a logged-in user.
# We'll override this per-view for public endpoints (product list, etc.).
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# --- SimpleJWT Configuration ---
# ACCESS_TOKEN_LIFETIME: short-lived (15 min) so a stolen token expires quickly.
# REFRESH_TOKEN_LIFETIME: longer-lived (7 days). Used only to get a new access token.
# ROTATE_REFRESH_TOKENS: each refresh call issues a new refresh token (rolling window).
# BLACKLIST_AFTER_ROTATION: the old refresh token is blacklisted so it can't be reused.
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# --- CORS ---
# CORS_ALLOWED_ORIGINS: only the React dev server is allowed to call our API.
# Without this, the browser would block the request as a cross-origin violation.
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite default dev server port
    'http://127.0.0.1:5173',
]


# --- Media Files ---
# MEDIA_ROOT: where uploaded files (product images) are saved on disk.
# MEDIA_URL: the URL prefix used to serve those files.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- Static Files ---
STATIC_URL = '/static/'


# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# BigAutoField uses 64-bit integers for primary keys.
# Default is 32-bit which can overflow on large tables — better to set this upfront.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
