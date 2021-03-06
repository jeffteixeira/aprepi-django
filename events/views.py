from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View, FormView)
from donations.views import MakeDonation
from users.models import Benefactor

from events.forms import EventDonationForm, EventForm
from events.models import Event


class EventCreateView(LoginRequiredMixin, CreateView):
    template_name = 'events/create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:list')


class EventListView(LoginRequiredMixin, ListView):

    model = Event
    template_name = 'events/list.html'

    def get_queryset(self):
        return Event.objects.all().order_by('-updated_at')


class EventDetailView(LoginRequiredMixin, DetailView):

    model = Event
    template_name = 'events/detail.html'


class EventUpdateView(LoginRequiredMixin, UpdateView):

    model = Event
    template_name = 'events/create.html'
    form = EventForm
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('events:detail', kwargs={'pk': self.object.id})


class EventDeleteView(LoginRequiredMixin, DeleteView):

    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy('events:list')


class MakeDonationEventView(MakeDonation):
    template_name = 'donations/make_donation.html'
    form_class = EventDonationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_event'] = True
        context['form_title'] = "FAZER DOAÇÃO PARA EVENTO"
        return context

    def form_valid(self, form):

        benefactor = get_object_or_404(Benefactor, pk=self.request.user)
        form.instance.benefactor = benefactor

        method = "CREDIT"
        form.instance.method = method
        donated_value = form.instance.donated_value

        form.instance.status = "approved"
        event_name = form.instance.event.event_name

        form.save()

        init_point = self.get_preference_id(donated_value, f"[Doação APREPI] {event_name}")

        return HttpResponseRedirect(init_point)
