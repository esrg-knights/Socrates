from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DiningParticipationThird


class DiningThirdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiningThirdForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Account aanmaken', css_class="btn-block"))
    class Meta:
        model = DiningParticipationThird
        exclude = ("added_by", "dining_list", "paid")
