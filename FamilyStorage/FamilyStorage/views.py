from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView, UpdateView

from FamilyStorage.forms import UserForm
from Person.models import PersonModel


@login_required
def connections_page(req):
    all_relatives_info = []

    for i in PersonModel.objects.filter(user__exact=req.user.id):
        info = {'person': (str(i), i.date_of_birth, i.date_of_death)}
        if i.mother:
            info.update({'mother': str(i.mother)})
        if i.father:
            info.update({'father': str(i.father)})
        all_relatives_info.append(info)

    import pydot

    graph = pydot.Dot('my_graph', graph_type='digraph',
                      suppress_disconnected=True, bgcolor='transparent')

    # Add nodes
    for i in all_relatives_info:
        name, birth, death = i['person']
        if not (birth or death):
            dates = ''
        else:
            dates = f"({birth or ''} / {death or ''})"
        person_info = f"{name}\n{dates}"
        my_node = pydot.Node(name, label=person_info, fontname='Arial')
        graph.add_node(my_node)

    for i in all_relatives_info:
        for j in ['mother', 'father']:
            parent = i.get(j)
            if parent:
                my_edge = pydot.Edge(i['person'][0], parent, color='black', style='dotted')
                graph.add_edge(my_edge)
    graph.write_png('/home/user/MyFolder/FamilyProject/FamilyStorage/static/graph.png')
    return render(req, 'connections_page.html')


def main_page(req):
    return render(req, 'main_page.html')


def sign_up(req):
    if req.POST:
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = UserForm()

    return render(req, 'registration/sign_up.html', {'form': form})


class UserInfoView(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'user_info.html'
    model = User
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super(UserInfoView, self).get(request, *args, **kwargs)


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('account')

    def get(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super().post(request, *args, **kwargs)


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('all_people')

    def get(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super().post(request, *args, **kwargs)
