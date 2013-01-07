from reservation.models import Reservation
from reservation.models import UserProfile
from django.http import Http404
from django.http import HttpResponse
<<<<<<< HEAD
from django.utils import timezone
=======
from django.views.generic import TemplateView


class ReservationView(TemplateView):
    template_name = 'reservation/index.html'

    def get_context_data(self):
        return {}

>>>>>>> 7cf05203d015ecc6e819c477b7c049f4e697a728

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
            date = timezone.now().date
            reservation = Reservation.objects.filter(user=user, date=date)
            if reservation:
                # already reserved
                return HttpResponse('You already reserved lunch, thanks!')
            profile.balance -= 10
            profile.save()
            Reservation.objects.create(user=user)
            msg = 'OK! Your reservation has been recorded. You balance is %s CNY.' % profile.balance
            return HttpResponse(msg)
    raise Http404()
