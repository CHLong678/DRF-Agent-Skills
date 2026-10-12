SECRET_KEY = "fixture-only"
DEBUG = True
ROOT_URLCONF = "project.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "fixtureapp",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
MIGRATION_MODULES = {"fixtureapp": None}
USE_TZ = True
