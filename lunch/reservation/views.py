from reservation.models import Reservation
from reservation.models import UserProfile
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response


class ReservationView(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('reservation/index.html',
                              {},
                              context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
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
                # date = timezone.now().date
                # reservation = Reservation.objects.filter(user=user, date=date)
                # if reservation:
                #     # already reserved
                #     return HttpResponse('You already reserved lunch, thanks!')
                profile.balance -= 10
                profile.save()
                Reservation.objects.create(user=user)
                msg = 'OK! Your reservation has been recorded. You balance is %s CNY.' % profile.balance
                return HttpResponse(msg)
        raise Http404()


# def reserve(request):
#     user = request.user
#     profile = None
#     try:
#         profile = UserProfile.objects.get(user=user)
#     except:
#         pass
#     if profile:
#         if profile.balance < 10:
#             return HttpResponse('Balance less than 10 CNY, please recharge')
#         else:
#             date = timezone.now().date
#             reservation = Reservation.objects.filter(user=user, date=date)
#             if reservation:
#                 # already reserved
#                 return HttpResponse('You already reserved lunch, thanks!')
#             profile.balance -= 10
#             profile.save()
#             Reservation.objects.create(user=user)
#             msg = 'OK! Your reservation has been recorded. You balance is %s CNY.' % profile.balance
#             return HttpResponse(msg)
#     raise Http404()
