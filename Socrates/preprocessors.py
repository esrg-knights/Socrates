import random

from news.models import Post


def basic_stats(request):
    setups = {
        "pre_page_name": "KOTKT",
    }

    return setups


def random_factor(request):
    val = random.randint(0, 100)
    ret = True if val == 1 else False

    return {"easter_egg_factor": ret}


def get_latest_news(request):
    return {'latest_post': Post.objects.all().first()}
