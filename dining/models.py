# Create your models here.
import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.datetime_safe import datetime


class DiningList(models.Model):
    relevant_date = models.DateField()
    owner = models.ForeignKey(User, related_name="owned_by", null=True, blank=True)
    closing_time = models.TimeField(default="14:00")

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

    def get_comments(self):
        print(DiningComment.objects.filter(dining_list=self))
        return DiningComment.objects.filter(dining_list=self)

    def user_in_list(self, user):
        return len(DiningParticipation.objects.filter(dining_list=self, user=user)) > 0

    def assign_dishes(self, randomChoices=True):
        """
        Assign new disheswashers
        :param randomChoices:
        :return:
        """
        dishes_already = DiningParticipation.objects.filter(dining_list=self, work_dishes=True).count()
        participations = DiningParticipation.objects.filter(dining_list=self, work_dishes=False, work_cook=False,
                                                            work_groceries=False)

        print(dishes_already)
        print(participations)
        new_dishes = []
        if randomChoices:
            while dishes_already != 3:
                # randomly pick someone
                try:
                    part = random.choice(participations)
                    new_dishes.append(part)

                    dishes_already += 1
                except:
                    break
        else:
            participations.order_by("-user_diningstats_get_percentage")

            print(", ".join([x.user.get_full_name() for x in participations]))
            new_dishes = participations[:3 - dishes_already]

        print(new_dishes)
        for disher in new_dishes:
            disher.work_dishes = True
            disher.save()

    def remove_user(self, user):
        DiningParticipation.objects.get(user=user, dining_list=self).delete()

        if user == self.owner:
            self.owner = None

        self.save()

    def get_allergies(self):
        return [x.get_allergy() for x in self.get_participants() if x.get_allergy() is not u""]

    def get_rather_nots(self):
        return [x.get_rather_not() for x in self.get_participants() if x.get_rather_not() is not u""]

    def __str__(self):
        return str(self.relevant_date)


class DiningParticipation(models.Model):
    dining_list = models.ForeignKey(DiningList)
    user = models.ForeignKey(User)
    added_by = models.ForeignKey(User, null=True, blank=True, related_name="addedby")

    work_dishes = models.BooleanField(default=False)
    work_cook = models.BooleanField(default=False)
    work_groceries = models.BooleanField(default=False)

    paid = models.BooleanField(default=False)

    def has_contributed(self):
        return self.work_cook is True or self.work_dishes is True

    def get_allergy(self):
        if self.user.detailsmodel.allergies is not u"":
            return u"{}: {}".format(self.user.get_full_name(), self.user.detailsmodel.allergies)
        else:
            return u""

    def get_rather_not(self):
        if self.user.detailsmodel.rather_nots is not u"":
            return u"{}: {}".format(self.user.get_full_name(), self.user.detailsmodel.rather_nots)
        else:
            return u""

    def cancel(self):
        send_mail("De eetlijst van {} is afgezegd".format(self.dining_list.relevant_date),
                  "Er is niemand gevonden die wil koken. Wil je dit toch doen? Stuur dan een berichtje naar het bestuur",
                  "watson@kotkt.nl", (self.user.email,))
        self.delete()

    class Meta:
        ordering = ("user__first_name",)


class DiningParticipationThird(models.Model):
    dining_list = models.ForeignKey(DiningList)
    added_by = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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

            if instance.work_cook:
                stats.total_helped -= 1

            if instance.work_dishes:
                stats.total_helped -= 1

            stats.total_participated -= 1

            stats.save()

    @receiver(post_save, sender=DiningParticipation)
    def add_new_scores(sender, instance=None, created=False, **kwargs):
        stats = DiningStats.objects.get_or_create(user=instance.user)[0]

        if instance.work_cook:
            stats.total_helped += 1

        if instance.work_dishes:
            stats.total_helped += 1

        stats.total_participated += 1

        stats.save()

    @receiver(post_delete, sender=DiningParticipation)
    def remove_old_participation(sender, instance=None, **kwargs):
        stats = DiningStats.objects.get_or_create(user=instance.user)[0]

        if instance.has_contributed():
            stats.total_helped -= 1

        stats.total_participated -= 1

        stats.save()


class DiningComment(models.Model):
    user = models.ForeignKey(User)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    dining_list = models.ForeignKey(DiningList)


class RecipeModel(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_last_edited = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=64)
    recipe = models.TextField()
    ingredients = models.TextField()
    allergies = models.TextField(default="")
    amount_of_people = models.IntegerField(default=4)

    visible = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_last_edited = datetime.now()

        super(RecipeModel, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ("name", "date_last_edited")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
