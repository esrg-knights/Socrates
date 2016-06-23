from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View

# Create your views here
from account.forms import LoginForm, RegisterForm, CompleteRegistrationForm, DetailsForm, \
    PasswordChangeRequestForm, PasswordChangeForm
from django.contrib.auth.models import Group
from account.models import DetailsModel, PasswordChangeRequestModel
from achievements.models import AchievementGet
from dining.models import DiningStats


class IndexView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {}

        context['dining_stats'] = DiningStats.objects.get_or_create(user=request.user)[0]
        context['achievements'] = AchievementGet.objects.filter(user=request.user)
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
        url = "http://app.kotkt.nl/accounts/activate/{0}".format(user.detailsmodel.uid)
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

        if user.is_active:
            messages.error(request, "Account is al geactiveerd")
            return redirect("dining:index")

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

        if user.is_active:
            messages.error(request, "Account is al geactiveerd")
            return redirect("dining:index")

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


class DetailsView(View):
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        if request.user.detailsmodel.is_softbanned:
            messages.error(request, request.user.detailsmodel.ban_reason)
            return redirect("account:index")
        self.context['form'] = DetailsForm(instance=request.user.detailsmodel)

        return render(request, "account/details.html", self.context)

    @method_decorator(login_required)
    def post(self, request):
        form = DetailsForm(request.POST, instance=request.user.detailsmodel)

        if form.is_valid():
            form.save()
            return self.get(request)

        self.context['form'] = form

        return render(request, "account/details.html", self.context)


class PasswordChangeView(View):
    context = {}
    template_name = "account/password_change.html"

    def get(self, request, token=None):
        if token is None:
            self.context['form'] = PasswordChangeRequestForm()
        else:
            self.context['form'] = PasswordChangeForm()

        return render(request, self.template_name, self.context)

    def post(self, request, token=None):
        if token is None:
            form = PasswordChangeRequestForm(request.POST)

            if form.is_valid():
                user = get_object_or_404(User, email=form.cleaned_data['email'])
                obj, ret = PasswordChangeRequestModel.objects.get_or_create(user=user)
                messages.success(request, "Successfully created a password change request")
                obj.send_change_mail()

                return redirect("account:index")
            else:
                self.contex['form'] = form
        else:
            form = PasswordChangeForm(request.POST)

            if form.is_valid():
                request_form = get_object_or_404(PasswordChangeRequestModel, token=token)

                request_form.user.set_password(form.cleaned_data['password'])

                request_form.user.save()

                messages.success(request, "Succesfully changed your password")

                request_form.delete()

                return redirect("account:index")
            else:
                self.context['form'] = form

        return render(request, self.template_name, self.context)


class GroupView(View):
    template_name = "account/groups.html"
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        self.context['groups'] = Group.objects.all()

        return render(request, self.template_name, self.context)


class MemberView(View):
    template = "account/members.html"
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        if request.user.groups.filter(name="Bestuur"):
            self.context['users'] = User.objects.all()

            return render(request, self.template, self.context)
        else:
            messages.error(request, "Je hebt hier geen rechten voor!")
            return redirect("account:index")
