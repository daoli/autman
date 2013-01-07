from django.views.generic import TemplateView


class ReservationView(TemplateView):
    template_name = 'reservation/index.html'

    def get_context_data(self):
        return {}
