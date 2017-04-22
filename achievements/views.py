from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View

from achievements.models import Achievement
from achievements.models import AchievementGet


class IndexView(View):
    template_name = "achievements/index.html"
    context = {}

    @method_decorator(login_required())
    def get(self, request):
        self.context['achievements'] = Achievement.objects.filter(is_public="true").order_by('-priority', 'name')
        self.context['gets'] = AchievementGet.objects.order_by('user__first_name').filter(achievement__is_public="true")

        return render(request, self.template_name, self.context)
