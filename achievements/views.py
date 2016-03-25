from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from achievements.models import Achievement


class IndexView(View):
    template_name = "achievements/index.html"
    context = {}

    def get(self, request):
        self.context['achievements'] = Achievement.objects.all()

        return render(request, self.template_name, self.context)
