from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import generic

from Person.forms import PersonModelForm
from Person.models import PersonModel


def person_info(req, pid):
    return render(req, 'person_info.html',
                  {'person': get_object_or_404(PersonModel, id=pid)})


def add_person(req):
    form = PersonModelForm(req.POST or None)

    if req.POST and form.is_valid():
        person = form.save(commit=True)
        return redirect(reverse('person_info', args=(person.id, )))

    return render(req, 'add_person.html', {'form': form})


def delete_person(req, pid):
    if req.POST:
        PersonModel.objects.filter(id=pid).delete()
    return redirect(reverse('all_persons'))


class PersonListView(generic.ListView):
    model = PersonModel
    context_object_name = 'persons_list'
    template_name = 'persons_list.html'
    paginate_by = 5


def update_person_info(req, pid, field):
    if req.POST:
        person = PersonModel.objects.filter(id=pid)
    #     action = req.POST.get('action')
    #     if action == '':
    #        person.update(first_name='test')

    return redirect(reverse('person_info', args=(PersonModel.objects.get(id=pid).id, )))
