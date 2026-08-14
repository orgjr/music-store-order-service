from .base import *

ENVIRONMENT = "prod"

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES = {"default": env.db("DATABASE_URL")}

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "HOST": env("SMTP_HOST", default="localhost"),
        "PORT": env.int("SMTP_PORT", default=587),
        "HOST_USER": env("SMTP_USER", default=""),
        "HOST_PASSWORD": env("SMTP_PASSWORD", default=""),
        "USE_TLS": env.bool("SMTP_USE_TLS", default=True),
    },
}
