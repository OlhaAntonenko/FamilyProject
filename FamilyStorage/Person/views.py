from django.shortcuts import get_object_or_404, redirect, render, reverse

from Person.forms import PersonModelForm
from Person.models import PersonModel


# Create your views here.
def all_persons(req):
    return render(req, 'all_persons.html',
                  {'persons': PersonModel.objects.all()})


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
