import random

import datetime
from django.utils import timezone

from dining.models import SpecialDateModel
from news.models import Post


def basic_stats(request):
    setups = {
        "pre_page_name": "KOTKT",
        "alerts": SpecialDateModel.objects.filter(date_implied=timezone.now().date())
    }

    return setups


def random_factor(request):
    val = random.randint(0, 100)
    ret = True if val == 1 else False

    return {"easter_egg_factor": ret}


def get_latest_news(request):
    cur_time = timezone.now()
    delta_time = datetime.timedelta(weeks=2)

    latest_post = Post.objects.all().first()
    if latest_post.date_posted + delta_time < cur_time:
        latest_post = None


    return {'latest_post': latest_post}
