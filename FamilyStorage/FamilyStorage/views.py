from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView, UpdateView

from FamilyStorage.forms import UserForm


@login_required
def home_page(req):
    return render(req, 'home_page.html')


def main_page(req):
    return render(req, 'main_page.html')


def sign_in(req):
    if req.POST:
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = UserForm()

    return render(req, 'registration/sign_in.html', {'form': form})


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
    success_url = reverse_lazy('all_persons')

    def get(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.kwargs.update({self.pk_url_kwarg: request.user.id})
        return super().post(request, *args, **kwargs)
