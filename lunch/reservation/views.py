from reservation.models import Reservation
from reservation.models import UserProfile
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


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
                profile.balance -= 10
                profile.save()
                Reservation.objects.create(user=user)

                date = timezone.now().date
                reservations = Reservation.objects.filter(date=date)
                msg = 'OK! Your reservation has been recorded. You balance is %s CNY. You ordered %s meals today.' % (profile.balance, reservations.count())
                return HttpResponse(msg)
        raise Http404()


def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect(reverse('resv:reservation', kwargs={}))
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    print state
    return render_to_response('reservation/login.html',{'state':state, 'username': username},
        context_instance=RequestContext(request))
