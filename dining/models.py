# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime


class DiningList(models.Model):
    relevant_date = models.DateField()
    owner = models.ForeignKey(User, related_name="owned_by", null=True, blank=True)
    closing_time = models.TimeField(default="15:00")

    def get_participants(self):
        return DiningParticipation.objects.filter(dining_list=self).prefetch_related()

    def get_thirds(self):
        return DiningParticipationThird.objects.filter(dining_list=self).prefetch_related()

    @staticmethod
    def get_latest():
        return DiningList.objects.get_or_create(relevant_date=datetime.now().date())[0]

    @staticmethod
    def get_specific_date(day, month, year):
        date = datetime(int(year), int(month), int(day))

        if date.date() > datetime.now().date():
            return DiningList.get_latest()

        return DiningList.objects.get_or_create(relevant_date=date)[0]

    def user_in_list(self, user):
        return len(DiningParticipation.objects.filter(dining_list=self, user=user)) > 0

    def remove_user(self, user):
        DiningParticipation.objects.get(user=user, dining_list=self).delete()

        if user == self.owner:
            self.owner = None

        self.save()

    def get_allergies(self):
        return [x.get_allergy() for x in self.get_participants() if x.get_allergy() is not ""]

    def __str__(self):
        return str(self.relevant_date)


class DiningParticipation(models.Model):
    dining_list = models.ForeignKey(DiningList)
    user = models.ForeignKey(User)

    work_dishes = models.BooleanField(default=False)
    work_cook = models.BooleanField(default=False)
    work_groceries = models.BooleanField(default=False)

    paid = models.BooleanField(default=False)

    def get_allergy(self):
        if self.user.detailsmodel.allergies is not "":
            stripped = (c for c in self.user.detailsmodel.allergies if 0 < ord(c) < 127)
            allergy = ''.join(stripped)
            return "{}: {}".format(self.user.get_full_name(), allergy)
        else:
            return ""

    class Meta:
        ordering = ("user__first_name",)


class DiningParticipationThird(models.Model):
    dining_list = models.ForeignKey(DiningList)
    added_by = models.ForeignKey(User)
    name = models.CharField(max_length=30)
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

        return round(float(self.total_helped) / self.total_participated * 100, 0)

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
