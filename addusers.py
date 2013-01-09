from django.contrib.auth.models import User
import random
import string
from reservation.models import UserProfile

names = [('username', 'email@example.com'),
         ]


def generate_pw(n=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(n))


for name, email in names:
    pw = generate_pw()
    user = User.objects.create_user(name, email, pw)
    print name, email, pw
    profile = UserProfile.objects.create(user=user)

