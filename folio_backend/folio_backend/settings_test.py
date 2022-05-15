import os

from folio_backend.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
ALLOWED_HOSTS.append("testserver")

# FIXTURE_DIRS = [
#     os.path.join(BASE_DIR, 'fixtures')
# ]
