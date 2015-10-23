from django.contrib.admin import site
from login.models import UserProfile

site.register(UserProfile)