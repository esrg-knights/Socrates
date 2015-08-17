from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib import messages

# Create your views here
from account.forms import LoginForm


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {}
        return render(request, 'account/index.html', context)


class LogoutView(View):
    def get(self, request):
        if request.user.is_active:
            logout(request)

            messages.success(request, "Uitloggen gelukt!")

            return redirect("account:login")

        messages.info(request, "Je bent nog niet eens ingelogd!")

        return redirect("account:login")


class LoginView(View):
    context  = {}
    template = "account/login.html"

    def get(self, request):
        if request.user.is_active:
            messages.info(request, "Je bent al ingelod!")
            return redirect("account:index")

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
                    if len(request.GET) > 0:
                        return redirect(request.GET['next'])
                    return redirect("account:index")
                else:
                    messages.error(request, "Deze account is niet geactiveerd")
            else:
                messages.warning(request, "Gebruikersnaam of wachtwoord klopt niet")

        self.context['form'] = form
        return render(request, self.template, self.context)
