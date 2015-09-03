# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class DiningList(models.Model):
    relevant_date = models.DateField(auto_now=True, auto_created=True)
    owner = models.ForeignKey(User, related_name="owned_by", null=True, blank=True)

    def get_participants(self):
        return DiningParticipation.objects.filter(dining_list=self)

    @staticmethod
    def get_latest():
        return DiningList.objects.get_or_create()[0]


class DiningParticipation(models.Model):
    dining_list = models.ForeignKey(DiningList)
    user = models.ForeignKey(User)

    work_dishes = models.BooleanField(default=False)
    work_cook = models.BooleanField(default=False)
    work_groceries = models.BooleanField(default=False)

    paid = models.BooleanField(default=False)


class DiningStats(models.Model):
    user = models.ForeignKey(User)

    total_participated = models.IntegerField(default=0)
    total_helped = models.IntegerField(default=0)

    def get_percentage(self):
        """
        Gets the helping out percentage
        :return: percentage  (79, 81)
        """
        if self.total_participated <= 5:
            return 100

        return abs(self.total_helped / self.total_participated * 100)

    @receiver(pre_save, sender=DiningParticipation)
    def remove_old_scores(sender, instance=None, created=False, **kwargs):
        if instance.id:
            instance = DiningParticipation.objects.get(id=instance.id)
            stats = DiningStats.objects.get_or_create(user=instance.user)[0]

            if instance.work_cook or instance.work_dishes:
                stats.total_helped -= 1

            stats.total_participated -= 1

            stats.save()

    @receiver(post_save, sender=DiningParticipation)
    def add_new_scores(sender, instance=None, created=False, **kwargs):
        stats = DiningStats.objects.get_or_create(user=instance.user)[0]

        if instance.work_cook or instance.work_dishes:
            stats.total_helped += 1

        stats.total_participated += 1

        stats.save()
