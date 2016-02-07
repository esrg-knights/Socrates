from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DiningParticipationThird, DiningParticipation, DiningList


class DiningThirdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiningThirdForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Registreren', css_class="btn-block"))

    class Meta:
        model = DiningParticipationThird
        exclude = ("added_by", "dining_list", "paid")


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class DiningThirdNewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DiningThirdNewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Registreren', css_class="btn-block"))

    user = UserChoiceField(queryset=User.objects.all(), required=False,
                                  help_text="Gebruiker die bij de eetlijst wil")

    third = forms.CharField(required=False, help_text="Niet lid die bij de eetlijst wil.")

    def save(self, request):
        """
        Tries to save a form like this
        :return:
        """
        dinnerlist = DiningList.get_latest()

        if self.data['user'] is not u"":
            obj, ret = DiningParticipation.objects.get_or_create(dining_list=dinnerlist, user=User.objects.get(id=self.data['user']))

            if ret:
                obj.added_by = request.user
                obj.save()
                messages.success(request, "Je hebt {} toegevoegd aan de eetlijst".format(obj.user.get_full_name()))
            else:
                messages.warning(request, "Deze gebruiker staat al op de eetlijst")
        else:
            obj, ret = DiningParticipationThird.objects.get_or_create(dining_list=dinnerlist, name=self.data['third'],
                                                                      added_by=request.user)

            if ret:
                messages.success(request, "{} is toegevoegd aan de eetlijst".format(self.data['third']))
            else:
                messages.warning(request, "je hebt deze persoon al toegevoegd")
