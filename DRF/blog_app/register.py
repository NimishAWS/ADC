import random

from .models import AuthUsers


def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not AuthUsers.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(1, 100))
        return generate_username(random_username)
