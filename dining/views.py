# Create your views here.
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from dining.models import DiningList, DiningParticipation


class IndexView(View):
    context = {}
    template = "dining/index.html"

    @method_decorator(login_required)
    def get(self, request, day=None, month=None, year=None):
        if day is not None:
            self.context['dinnerlist'] = DiningList.get_specific_date(day, month, year)
        else:
            self.context['dinnerlist'] = DiningList.get_latest()

        self.context['participants'] = self.context['dinnerlist'].get_participants()

        return render(request, self.template, self.context)

    @method_decorator(login_required)
    def post(self, request, day=None, month=None, year=None):
        regex_filter = r'(\d+):(\w+)'

        # todo: secure this
        post = request.POST

        # first we'll clear all current statusses

        dinnerlist = DiningList.get_latest()

        participants = dinnerlist.get_participants()

        for part in participants:
            part.work_groceries = False
            part.work_cook = False
            part.work_dishes = False

            part.save()

        for key in post.keys():
            m = re.match(regex_filter, key)

            if m:
                part = [x for x in participants if x.id == int(m.group(1))][0]

                if m.group(2) == "groceries":
                    part.work_groceries = True
                if m.group(2) == "cooking":
                    part.work_cook = True
                if m.group(2) == "dishes":
                    part.work_dishes = True
                if m.group(2) == "paid":
                    part.paid = True

                messages.info(request, "{0} is opgeslagen als {1}".format(part.user.get_full_name(), m.group(2)))

        for part in participants:
            part.save()

        messages.success(request, "Behandelingen zijn successvol doorgevoerd")

        return redirect("dining:index")


class RegisterView(View):
    @method_decorator(login_required)
    def get(self, request):
        dinnerlist = DiningList.get_latest()

        # See if the user is already registered
        obj, ret = DiningParticipation.objects.get_or_create(user=request.user, dining_list=dinnerlist)

        if ret:
            messages.success(request, "Je bent succesvol ingeschreven voor deze eetlijst")
        else:
            messages.info(request, "Je was al ingeschreven voor deze lijst")

        return redirect("dining:index")


class ClaimView(View):
    template = "base.html"
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        dining_list = DiningList.get_latest()

        if dining_list.owner is not None:
            messages.error(request, "Deze eetlijst is al geclaimd door {0}".format(dining_list.owner.get_full_name()))
        else:
            # check participation
            if DiningParticipation.objects.filter(user=request.user, dining_list=dining_list).count() > 0:
                messages.success(request, "Je bent nu eigenaar van deze eetlijst!")
                dining_list.owner = request.user
                dining_list.save()
            else:
                messages.warning(request, "Je bent nog niet ingeschreven voor deze eetlijst! Doe dit eerst")

        return redirect("dining:index")
