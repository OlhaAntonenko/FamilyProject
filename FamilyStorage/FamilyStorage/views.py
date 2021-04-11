from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

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
