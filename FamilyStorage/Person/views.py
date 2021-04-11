from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from Person.models import PersonModel


class PersonInfoView(generic.detail.DetailView):
    template_name = 'person_info.html'
    model = PersonModel
    context_object_name = 'person'


class PersonListView(LoginRequiredMixin, generic.ListView):
    model = PersonModel
    context_object_name = 'persons_list'
    template_name = 'persons_list.html'


class PersonCreate(LoginRequiredMixin, CreateView):
    model = PersonModel
    fields = '__all__'


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = PersonModel
    fields = '__all__'


class PersonDelete(LoginRequiredMixin, DeleteView):
    model = PersonModel
    success_url = reverse_lazy('all_persons')

