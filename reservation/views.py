from reservation.models import RechargeHistory
from reservation.models import Reservation
from reservation.models import UserProfile
from django.utils import timezone
from django.views.generic import View
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def _get_information(request):
        data = {}
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if profile.balance < 10:
            msg = 'Balance less than 10 CNY, please recharge'
            data['msg'] = msg

        date = timezone.now().date
        user_reservations = Reservation.objects.filter(user=user, date=date)
        total_reservations = Reservation.objects.filter(date=date)

        data.update({
            'user': user,
            'profile': profile,
            'user_count_today': user_reservations.count(),
            'total_count_today': total_reservations.count(),
        })

        return data


class ChargeHistoryView(TemplateView):
    template_name = 'reservation/charge_history.html'

    def get_context_data(self):
        histories = RechargeHistory.objects.filter(user=self.request.user)
        context_data = _get_information(self.request)
        context_data.update({
            'histories': histories,
        })
        return context_data


class ReservationView(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('reservation/index.html',
                              _get_information(request),
                              context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        user = request.user

        profile = UserProfile.objects.get(user=user)
        if profile.balance >= 10:
            profile.balance -= 10
            profile.save()
            Reservation.objects.create(user=user)

        return HttpResponseRedirect(reverse('resv:reservation', kwargs={}))


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

    return render_to_response('reservation/login.html', {'state': state, 'username': username},
        context_instance=RequestContext(request))
