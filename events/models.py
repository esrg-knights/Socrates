import datetime

from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    # onderstaande is geen reference naar een group. Dat moet het wel zijn, alleen ivm afwezige inwendige id gaat dit verkeerd.
    #group = models.CharField(max_length=200, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    remark = models.TextField(max_length=200, blank=True)
    date = models.DateTimeField(help_text="The planned date")
    display_time = models.BooleanField(help_text="Whether the inserted time should be used")
    is_public = models.BooleanField(help_text="Whether it is shown to all")
    location = models.CharField(max_length=50, blank=True)
    category = models.SmallIntegerField(choices=(
        (1, ""),
        (2, "Lange Bordspeldag"),
        (3, "Zwaardvechttrainingen"),
        (4, "Ledenactiviteit"),
        (5, "Belangrijk"),
    ), default=1, help_text="Selector voor type event")

    def get_visual_date(self):
        week = "Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"
        maand = "Januari", "Februari", "Maart", "April", "Mei", "Juni", "Juli", "Augustus", "September", "Oktober", "November", "December"
        result =                week[self.date.weekday()]
        result = result + " " + str(self.date.day)
        result = result + " " + maand[self.date.month - 1]
        if self.display_time:
            if self.date.minute <10:
                result = result + " - " + str(self.date.hour) + ":0" + str(self.date.minute)
            else:
                result = result + " - " + str(self.date.hour) + ":" + str(self.date.minute)
        return result

    def get_short_visual_date(self):
        maand = "Januari", "Februari", "Maart", "April", "Mei", "Juni", "Juli", "Augustus", "September", "Oktober", "November", "December"
        result =                str(self.date.day)
        result = result + " " + maand[self.date.month - 1]
        return result

    def is_nearby(self):
        cur_time = timezone.now()

            # If the date is before today (correction inserted for events set earlier that day)
        if self.date <= cur_time - datetime.timedelta(hours=cur_time.hour):
            return 0

        # todo: implement if user wants to see certain events
        if 4 > 5:
            return 0

        if self.category < 4:
            maxTime = datetime.timedelta(weeks=2)
        if self.category == 4:
            maxTime = datetime.timedelta(weeks=2)
        if self.category == 5:
            maxTime = datetime.timedelta(weeks=2)

        return self.date - maxTime <= cur_time

    def __str__(self):
        return self.name