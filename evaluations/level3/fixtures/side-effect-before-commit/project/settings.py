SECRET_KEY = "fixture-only"
DEBUG = True
INSTALLED_APPS = ["django.contrib.auth","django.contrib.contenttypes","fixtureapp"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3","NAME": ":memory:"}}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
MIGRATION_MODULES = {"fixtureapp": None}
USE_TZ = True
