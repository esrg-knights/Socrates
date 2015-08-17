from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

# Create your views here
from account.forms import LoginForm


class IndexView(View):
    def get(self, request):
        context = {}
        messages.info(request, "test")
        return render(request, 'base.html', context)


class LoginView(View):
    context  = {}
    template = "account/login.html"

    def get(self, request):
        form = LoginForm()
        self.context['form'] = form
        return render(request, self.template, self.context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Inloggen gelukt!")
                    return redirect("account:index")
                else:
                    messages.error(request, "Deze account is niet geactiveerd")
            else:
                messages.warning(request, "Gebruikersnaam of wachtwoord klopt niet")

        self.context['form'] = form
        return render(request, "base.html", self.context)
