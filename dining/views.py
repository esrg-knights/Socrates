# Create your views here.
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views.generic import View

from dining.forms import DiningThirdForm, DiningThirdNewForm, CommentForm
from dining.models import DiningList, DiningParticipation, DiningStats


class IndexView(View):
    context = {}
    template = "dining/index.html"

    @method_decorator(login_required)
    def get(self, request, day=None, month=None, year=None):
        if day is not None:
            self.context['dinnerlist'] = DiningList.get_specific_date(day, month, year)
        else:
            self.context['dinnerlist'] = DiningList.get_latest()

        self.context['comments'] = self.context['dinnerlist'].get_comments()
        self.context['my_participation'] = True if DiningParticipation.objects.filter(user=request.user,
                                                                                      dining_list=self.context[
                                                                                          'dinnerlist']).count() == 1 else False
        self.context['participants'] = self.context['dinnerlist'].get_participants().prefetch_related()
        self.context['thirds'] = self.context['dinnerlist'].get_thirds()

        self.context['total'] = self.context['thirds'].count() + self.context['participants'].count()

        return render(request, self.template, self.context)

    @method_decorator(login_required)
    def post(self, request, day=None, month=None, year=None):
        regex_filter = r'(\d+):(\w+)'

        # todo: secure this
        post = request.POST

        # first we'll clear all current statusses

        dinnerlist = DiningList.get_latest()

        participants = dinnerlist.get_participants().select_related()

        for part in participants:
            part.work_groceries = False
            part.work_cook = False
            part.work_dishes = False

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

        for part in participants:
            part.save()

        messages.success(request, "Behandelingen zijn successvol doorgevoerd")

        return redirect("dining:index")


class RegisterView(View):
    @method_decorator(login_required)
    def get(self, request):
        dinnerlist = DiningList.get_latest()

        # 14:00 vanwege tijdzones

        if datetime.now().time() > dinnerlist.closing_time:
            messages.error(request, "De eetlijst is officieel gesloten. Vraag aan de koks of je er nog op mag")
        else:
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
        elif request.user.detailsmodel.is_softbanned:
            messages.error(request, "Je bent tijdelijk gebanned vanwege de volgende reden: {0}".format(request.user.detailsmodel.ban_reason))
        else:
            # check participation
            if DiningParticipation.objects.filter(user=request.user, dining_list=dining_list).count() > 0:
                messages.success(request, "Je bent nu eigenaar van deze eetlijst!")
                dining_list.owner = request.user
                dining_list.save()
            else:
                messages.warning(request, "Je bent nog niet ingeschreven voor deze eetlijst! Doe dit eerst")

        return redirect("dining:index")


class RemoveView(View):
    context = {}

    @method_decorator(login_required())
    def get(self, request):
        dining_list = DiningList.get_latest()

        if dining_list.owner is not None and datetime.now().time() > dining_list.closing_time:
            messages.error(request, "De eetlijst is al geclaimed. Vraag aan de kok/bestuur of je er nog af mag.")
            return redirect("dining:index")

        if dining_list.user_in_list(request.user):
            dining_list.remove_user(request.user)
            messages.success(request, "Je bent uitgeschreven van deze eetlijst")
        else:
            messages.error(request, "Je staat nog niet op deze eetlijst")

        return redirect("dining:index")


class StatView(View):
    template = "dining/stats.html"
    context = {}

    @method_decorator(user_passes_test(lambda u: u.is_superuser, "/dining/"))
    def get(self, request):
        self.context['stats'] = DiningStats.objects.all().order_by('total_participated')
        return render(request, self.template, self.context)


class AddThirdView(View):
    template = "dining/third.html"
    context = {}

    @method_decorator(login_required)
    def get(self, request):
        dinnerlist = DiningList.get_latest()

        if datetime.now().time() > dinnerlist.closing_time and request.user is not dinnerlist.owner:
            messages.error(request, "De eetlijst is officieel gesloten. Vraag aan de koks of je er nog op mag")
            return redirect("dining:index")

        self.context['form'] = DiningThirdNewForm()

        return render(request, self.template, self.context)

    @method_decorator(login_required)
    def post(self, request):
        form = DiningThirdNewForm(request.POST)

        if form.is_valid():
            form.save(request)

        self.context['form'] = form

        return render(request, self.template, self.context)


class CancelView(View):
    @method_decorator(login_required())
    def get(self, request):
        if not request.user.is_superuser:
            messages.error("Je hebt hier geen privileges voor!")
            return redirect("dining:index")
        send_mail("Eetlijst is afgezegd", "{} heeft deze afgezegd".format(request.user.get_full_name()),
                  "watson@kotkt.nl", ("bestuur@kotkt.nl",))
        [part.cancel() for part in DiningList.get_latest().get_participants()]

        messages.success(request, "Eetlijst is afgezegd")

        return redirect("dining:index")

class CommentView(View):
    context = {}

    template_name = "dining/comment.html"
    @method_decorator(login_required)
    def get(self, request):
        self.context['form'] = CommentForm()

        return render(request, self.template_name, self.context)

    @method_decorator(login_required())
    def post(self, request):
        form = CommentForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.dining_list = DiningList.get_latest()

            obj.save()

            messages.success(request, "Comment posted")

            return redirect("dining:index")

        self.context['form'] = form

        return render(request, self.template_name, self.context)