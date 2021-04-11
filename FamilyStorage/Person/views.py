from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import generic

from Person.forms import PersonModelForm
from Person.models import PersonModel


@login_required
def person_info(req, pid):
    return render(req, 'person_info.html',
                  {'person': get_object_or_404(PersonModel, id=pid)})


@login_required
def add_person(req):
    form = PersonModelForm(req.POST or None)

    if req.POST and form.is_valid():
        person = form.save(commit=True)
        return redirect(reverse('person_info', args=(person.id, )))

    return render(req, 'add_person.html', {'form': form})


@login_required
def delete_person(req, pid):
    if req.POST:
        PersonModel.objects.filter(id=pid).delete()
    return redirect(reverse('all_persons'))


class PersonListView(LoginRequiredMixin, generic.ListView):
    model = PersonModel
    context_object_name = 'persons_list'
    template_name = 'persons_list.html'


@login_required
def update_person_info(req, pid, field):
    if req.POST:
        person = PersonModel.objects.filter(id=pid)
    #     action = req.POST.get('action')
    #     if action == '':
    #        person.update(first_name='test')

    return redirect(reverse('person_info', args=(PersonModel.objects.get(id=pid).id, )))
