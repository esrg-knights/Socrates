from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from news.models import Post


class IndexView(View):
    template_name = "news/index.html"
    context = {}

    def get(self, request):
        self.context['posts'] = Post.objects.all()

        return render(request, self.template_name, self.context)