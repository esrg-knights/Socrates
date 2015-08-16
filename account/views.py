from django.shortcuts import render
from django.views.generic import View

# Create your views here
class IndexView(View):
    def get(self, request):
        context = {}
        return render(request, 'base.html', context)