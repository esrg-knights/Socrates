from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib import messages

# Create your views here
from account.forms import LoginForm, RegisterForm, CompleteRegistrationForm
from account.models import DetailsModel


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

            return redirect("dining:index")

        messages.info(request, "Je bent nog niet eens ingelogd!")

        return redirect("account:login")


class LoginView(View):
    context = {}
    template = "account/login.html"

    def get(self, request):
        if request.user.is_active:
            messages.info(request, "Je bent al ingelogd!")
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
                    return redirect("dining:index")
                else:
                    messages.error(request, "Deze account is niet geactiveerd")
            else:
                messages.warning(request, "Gebruikersnaam of wachtwoord klopt niet")

        self.context['form'] = form
        return render(request, self.template, self.context)


class RegisterView(View):
    context = {}
    template = "account/register.html"

    def send_registation_email(self, user):
        subject = "Registratie afmaken"
        url = "http://app.kotkt.nl/account/activate/{0}".format(user.detailsmodel.uid)
        body = "Je hebt je geregistreerd bij de Knights. Maak deze registratie af door naar het volgende adres te navigeren: {0}".format(
            url)

        user.email_user(subject, body, from_email="watson@kotkt.nl")

    def get(self, request):
        form = RegisterForm()

        self.context['form'] = form
        return render(request, self.template, self.context)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['password_repeat'] == form.cleaned_data['password']:
                user = form.save()

                details = DetailsModel()
                details.related_user = user
                details.save()

                self.send_registation_email(user)

                messages.success(request,
                                 "Er is een verificatie email gestuurd naar je emailadres. Kijk hier eerst naar")


                return redirect("account:login")

            messages.error(request, "De wachtwoorden kwamen niet overeen!")

        self.context['form'] = form

        return render(request, self.template, self.context)


class ActivationView(View):
    context = {}
    template = "account/activate.html"

    def get(self, request, user_hash):
        user = self.get_user(user_hash)

        self.context['new_user'] = user
        form = CompleteRegistrationForm(instance=user.detailsmodel)

        self.context['form'] = form
        return render(request, self.template, self.context)

    def get_user(self, user_id):
        try:
            return User.objects.get(detailsmodel__uid=user_id)
        except:
            raise Http404

    def post(self, request, user_hash):
        user = self.get_user(user_hash)

        form = CompleteRegistrationForm(request.POST, instance=user.detailsmodel)

        if form.is_valid():
            details = form.save(commit=False)

            details.related_user = user
            details.related_user.is_active = False
            details.related_user.save()
            details.save()

            user.is_active = True
            user.save()

            messages.success(request, "Je account is geactiveerd!")
            return redirect("account:login")

        self.context['form'] = form

        return render(request, self.template, self.context)
