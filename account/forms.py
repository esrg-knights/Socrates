from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User

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

class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Wachtwoord (herhaald)"
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Account aanmaken', css_class="btn-block"))

    class Meta:
        model = User
        exclude = (
        "id", "last_login", "is_superuser", "groups", "user_permissions", "is_staff", "is_active", "date_joined")
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
