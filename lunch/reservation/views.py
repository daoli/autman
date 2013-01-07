# Create your views here.
from reservation.models import Reservation
from reservation.models import UserProfile
from django.http import Http404
from django.http import HttpResponse

def reserve(request):
	user = request.user
	profile = None
	try:
		profile = UserProfile.objects.get(user=user)
	except:
		pass
	if profile:
		if profile.balance < 10:
			return HttpResponse('Balance less than 10 CNY, please recharge')
		else:
			profile.balance -= 10
			profile.save()
			Reservation.objects.create(user=user)
			return HttpResponse('OK!')
	raise Http404()
