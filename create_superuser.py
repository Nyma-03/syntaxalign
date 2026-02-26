import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# CHANGE THESE to whatever username/email/password you want
USERNAME = "meem3"
EMAIL = "meemtabassum246@gmail.com"
PASSWORD = "meem3"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("Superuser created!")
else:
    print("Superuser already exists")