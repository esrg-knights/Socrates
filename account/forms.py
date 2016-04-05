import re

from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field, HTML
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from account.models import DetailsModel


class LoginForm(forms.Form):
    username = forms.CharField(
            label="Gebruikersnaam",
            max_length=80,
            required=True,
    )

    password = forms.CharField(
            widget=forms.PasswordInput,
            label="Wachtwoord",
            required=True
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
                Field("username"),
                Field("password"),

                FormActions(
                        Submit('log_in', 'Log In', css_class=" btn-primary btn-block"),
                )
        )


class CompleteRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompleteRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Account aanmaken', css_class="btn-block"))

    class Meta:
        model = DetailsModel
        exclude = ('related_user',)


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        # You can dynamically adjust your layout
        self.helper.add_input(Submit('submit', 'Register', css_class="btn-block"))

    username = forms.CharField(
            label="Gebruikersnaam",
            widget=forms.TextInput(attrs={
                'id': 'username'}
            ),
            help_text="/[0-z-+.]+/",
            error_messages={
                'characters': "You used characters that were not allowed. The following are allowed: 0-9 A-z . + -.",
                'taken': "Your username has already been taken. Please try another one!"
            }
    )
    password = forms.CharField(
            label="Wachtwoord",
            widget=forms.PasswordInput(attrs=
            {
                'id': 'password'
            }),
            error_messages=
            {
                'mismatch': "Your password did not match the repeated password!",
                'length': "Your password needs to be at least 8 characters long",
                'digit': "Your password needs to contain at least 1 digit",
                'character': "Your password needs at least 1 letter",
            }
    )
    password_repeat = forms.CharField(
            label="Wachtwoord (Herhaald)",
            widget=forms.PasswordInput()
    )
    email = forms.CharField(
            label="Email",
            widget=forms.EmailInput(),
            error_messages=
            {
                'repeat': 'Your repeated email address did not match. Please make sure they are the same'
            }
    )
    email_repeat = forms.CharField(
            label="Email (Herhaald)",
            widget=forms.EmailInput()
    )
    first_name = forms.CharField(
            label="Voornaam"
    )
    last_name = forms.CharField(
            label="Achternaam"
    )

    def clean(self):
        try:
            assert self.cleaned_data['password'] is not None
            assert self.cleaned_data['password_repeat'] is not None
            assert self.cleaned_data['email'] is not None
            assert self.cleaned_data['email_repeat'] is not None
        except:
            raise ValidationError("Some fields were not filled in"
                                  "")
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise ValidationError(self.fields['password'].error_messages['mismatch'])
        if self.cleaned_data['email'] != self.cleaned_data['email_repeat']:
            raise ValidationError(self.fields['email'].error_messages['repeat'])
        if len(self.cleaned_data['password']) < 8:
            raise ValidationError(self.fields['password'].error_messages['length'])
        if not any(char.isdigit() for char in self.cleaned_data['password']):
            raise ValidationError(self.fields['password'].error_messages['digit'])
        if not any(char.isalpha() for char in self.cleaned_data['password']):
            raise ValidationError(self.fields['password'].error_messages['character'])

    def clean_username(self):
        if re.findall("[0-z-+.]+", self.cleaned_data['username'])[0] != self.cleaned_data['username']:
            raise ValidationError(self.fields['username'].error_messages['characters'])

        if len(User.objects.filter(username=self.cleaned_data['username'])) > 0:
            raise ValidationError(self.fields['username'].error_messages['taken'])

        return self.cleaned_data['username']

    def save(self):
        user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
        )

        user.is_active = False

        user.save()

        return user


class DetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            HTML("<h3>Persoonsgegevens</h3>"),
            "straat",
            "woonplaats",
            "postcode",
            "telefoonnummer",
            "geboortedatum",
            HTML("<h3>Schoolgegevens</h3>"),
            "instituut",
            "kaartnummer",
            HTML("<h3>Eetlijst</h3>"),
            "allergies",
            "rather_nots",
            "nickname",
        )

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Opslaan', css_class="btn-block"))

    class Meta:
        model = DetailsModel
        exclude = ("related_user",)


class PasswordChangeRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Opslaan', css_class="btn-block"))

    email = forms.EmailField(
            label="Email adres"
    )


class PasswordChangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Opslaan', css_class="btn-block"))

    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(PasswordChangeForm, self).clean()
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise ValidationError("Passwords did not match")
