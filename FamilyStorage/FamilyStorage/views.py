from django.shortcuts import get_object_or_404, redirect, render, reverse


def main_page(req):
    return render(req, 'main_page.html')
