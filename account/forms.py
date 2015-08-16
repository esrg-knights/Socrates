from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from crispy_forms.helper import FormHelper


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


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Gebruikersnaam",
        required=True,
        max_length=80
    )

    email = forms.EmailField(
        required=True,
        label="Email"
    )

    first_name = forms.CharField(
        required=True,
        label="Voornaam"
    )

    last_name = forms.CharField(
        required=True,
        label="Achternaam"
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Wachtwoord"
    )

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

        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            Field("first_name"),
            Field("last_name"),
            Field("password", css_class="password-field"),
            Field("password_repeat"),

            Submit("submit", "Submit", css_class="btn-primary btn-block")
        )
