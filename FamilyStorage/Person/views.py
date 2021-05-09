from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, FormMixin
from django.forms.models import model_to_dict

from FamilyStorage.settings import MEDIA_DIR, STATIC_DIR
from Person.forms import PersonModelForm
from Person.helpers import get_pdf_name
from Person.models import PersonModel
from django.http import FileResponse, HttpResponse, HttpResponseRedirect


class PersonInfoView(FormMixin, LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'person_info.html'
    model = PersonModel
    context_object_name = 'person'
    form_class = PersonModelForm

    def get(self, request, *args, **kwargs):
        response = super(PersonInfoView, self).get(request, *args, **kwargs)

        self.request.session['post_name'] = ''
        self.request.session['object_id'] = response.context_data['object'].id
        self.request.session['edit_data'] = []

        if request.user == response.context_data['object'].user:
            return response
        else:
            return redirect(reverse('main_page'))

    def get_success_url(self):
        return reverse("person_info", args=[self.get_object().id])

    def get_context_data(self, **kwargs):
        ctx = super(PersonInfoView, self).get_context_data(**kwargs)
        ctx["form"] = self.get_form()
        ctx["post_name"] = self.request.session.get('post_name')
        ctx["object_id"] = self.request.session.get('object_id')
        ctx["edit_data"] = self.request.session.get('edit_data')
        return ctx

    def get_initial(self):
        return ({"event": self.get_object(), 'user': self.request.user})

    def post(self, request, *args, **kwargs):
        req_keys = list(request.POST.keys())

        self.object = self.get_object()

        edit_data = [i.replace('edit__', '') for i in req_keys if 'edit__' in i]
        if edit_data:
            request.session['post_name'] = 'edit'
            request.session['object_id'] = self.object.id
            request.session['edit_data'] = edit_data
            return redirect(reverse("person_info", args=[self.object.id]))

        data = model_to_dict(self.object)
        data.update(request.POST.dict())
        files = request.FILES.dict()

        form = self.form_class(data, files, instance=self.object)

        delete_data = [i.replace('delete__', '') for i in req_keys if 'delete__' in i]
        for field in delete_data:
            field_data = getattr(form.instance, field)
            if field_data:
                (MEDIA_DIR / str(field_data)).unlink(missing_ok=True)
            field_data.delete()

        request.session['post_name'] = 'field'
        request.session['object_id'] = self.object.id
        request.session['edit_data'] = []

        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PersonListView(LoginRequiredMixin, generic.ListView):
    model = PersonModel
    context_object_name = 'people_list'
    template_name = 'people_list.html'

    def get_queryset(self):
        return PersonModel.objects.filter(user__exact=self.request.user.id)

    @staticmethod
    def post(req, *args, **kwargs):
        if req.POST.get('search'):
            person_url = req.POST.get('person_url')
            if person_url:
                return HttpResponseRedirect(person_url)
        return HttpResponseRedirect(reverse_lazy('all_people'))


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


class PersonDelete(LoginRequiredMixin, DeleteView):
    model = PersonModel
    success_url = reverse_lazy('all_people')


def download(request, pk):
    person = PersonModel.objects.get(id=pk)
    pdf_link = get_pdf_name(str(person), person.get_data())

    link = MEDIA_DIR / f'pdf/{pdf_link}'
    if link.is_file():
        response = FileResponse(open(link, 'rb'))
        return response
    else:
        return HttpResponse('<h3>Can not to create file</h3>')

