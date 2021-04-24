from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from Person.forms import PersonModelForm
from Person.models import PersonModel


class PersonInfoView(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'person_info.html'
    model = PersonModel
    context_object_name = 'person'

    def get(self, request, *args, **kwargs):
        response = super(PersonInfoView, self).get(request, *args, **kwargs)
        if request.user == response.context_data['object'].user:
            return response
        else:
            return redirect(reverse('main_page'))


class PersonListView(LoginRequiredMixin, generic.ListView):
    model = PersonModel
    context_object_name = 'persons_list'
    template_name = 'persons_list.html'

    def get_queryset(self):
        return PersonModel.objects.filter(user__exact=self.request.user.id)


class PersonCreate(LoginRequiredMixin, CreateView):
    model = PersonModel
    form_class = PersonModelForm

    def post(self, request, *args, **kwargs):
        data = request.POST

        _mutable_old_state = data._mutable
        data._mutable = True
        data['user'] = request.user
        data._mutable = _mutable_old_state

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.initial.update({'user': request.user})
        return super().get(request, *args, **kwargs)


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = PersonModel
    form_class = PersonModelForm
    success_url = reverse_lazy('all_persons')

    def get(self, request, *args, **kwargs):
        self.initial.update({'user': request.user})
        return super().get(request, *args, **kwargs)


class PersonDelete(LoginRequiredMixin, DeleteView):
    model = PersonModel
    success_url = reverse_lazy('all_persons')

