from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View

from achievements.models import Achievement



class IndexView(View):
    template_name = "snippets/test_page.html"
    context = {}

    @method_decorator(login_required())
    def get(self, request):
        self.context['achievements'] = Achievement.objects.all()

        return render(request, self.template_name, self.context)