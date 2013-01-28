from django.contrib.auth.models import User
import random
import string
import sys
from reservation.models import UserProfile


def generate_pw(n=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(n))


def add_user(name, email):
    pw = generate_pw()
    user = User.objects.create_user(name, email, pw)
    profile = UserProfile.objects.create(user=user)
    print 'User %s added with password: %s' % (name, pw)


if __name__ == '__main__':
	name = sys.argv[1]
	email = sys.argv[2]
	add_user(name, email)
