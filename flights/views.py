"""Module which contains all views of flights app."""
import datetime

from dal import autocomplete
from taggit.models import Tag

from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, DetailView, View, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from ants.views import add_iframe_to_context
from .forms import FlightForm, FlightStaffForm
from .models import Flight


# Create your views here.
@method_decorator(xframe_options_exempt, name='dispatch')
class AddFlightView(FormView):
    """View for adding a new flight."""
    template_name = 'flights/flights_add.html'
    success_url = reverse_lazy('flights_map')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY_CLIENT
        add_iframe_to_context(context, self.request)
        return context

    def form_valid(self, form):
        form.create_flight(self.request.user.is_staff)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        iframe = self.request.GET.get('iframe', None)
        kwargs['iframe'] = iframe
        return kwargs
    
    def get_form_class(self):
        if self.request.user.is_staff:
            return FlightStaffForm
        
        return FlightForm
    
    def get_success_url(self):
        iframe = self.request.GET.get('iframe', None)
        url = reverse_lazy('flights_map')
        
        if iframe:
            return url + '?iframe=true'
        
        return url

@method_decorator(xframe_options_exempt, name='dispatch')
class FlightsMapView(TemplateView):
    """View for the flights map."""
    template_name = 'flights/flights_map.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY_CLIENT
        context['years'] = [
            d.year for d in Flight.objects.all().dates('date', 'year', order='DESC')
        ]
        now = datetime.datetime.now()
        context['current_year'] = now.year
        add_iframe_to_context(context, self.request)
        return context

class FlightsListView(ListView):
    """List view for flights."""
    model = Flight
    # queryset = Flight.objects.filter(reviewed=True)
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        year = request.GET.get('year')
        if year and year != 'all':
            qs = qs.filter(date__year=year)
        data = [{
            'id': flight.id,
            'lat': flight.latitude,
            'lng': flight.longitude,
            'ant': flight.ant_species.name
        } for flight in qs]
        return JsonResponse(data, status=200, safe=False)


class FlightInfoWindow(DetailView):
    """View for google maps info window."""
    template_name = 'flights/info_window.html'
    model = Flight
    context_object_name = 'flight'

@method_decorator(staff_member_required, name='dispatch')
class FlightsReviewListView(ListView):
    """Displays all not yet reviewed flights."""
    model = Flight
    template_name = "flights/flights_review.html"
    queryset = model.objects.filter(reviewed=False)
    context_object_name = 'flights'

@method_decorator(staff_member_required, name='dispatch')
class FlightReviewView(View):
    def post(self, request, **kwargs):
        """Handels the post request."""
        pk = kwargs.get('pk')
        flight = get_object_or_404(Flight, pk=pk)
        flight.reviewed = True
        flight.save()

        return redirect('flights_review_list')

@method_decorator(staff_member_required, name='dispatch')
class FlightDeleteView(DeleteView):
    model = Flight
    success_url = reverse_lazy('flights_review_list')

class FlightStatisticView(TemplateView):
    template_name = 'flights/flight_statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ants = Flight.objects.values('ant_species__slug', 'ant_species__name') \
            .distinct().order_by('ant_species__name')
        context['ants'] = ants
        return context

class HabitatTagAutocomplete(autocomplete.Select2QuerySetView):
    """QuerySetView for flight habitat autocomplete."""
    def get_queryset(self):
        flight_content_type = ContentType.objects.get(app_label='flights', model='flight')
        qs = Tag.objects.filter(taggit_taggeditem_items__content_type=flight_content_type)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs.distinct().order_by('name')
