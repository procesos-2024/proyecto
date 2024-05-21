from django.shortcuts import render, redirect
from django.views.generic import FormView

from .forms import UserRegisterForm


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
