# Create your tests here.
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase
from django.utils.timezone import datetime

from dining.models import DiningStats, DiningList, DiningParticipation


class DiningStatsTest(SimpleTestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("test", "test", "test@test.com")
        self.testUser.save()

    def tearDown(self):
        self.testUser.delete()

    def test_get_percentage(self):
        stats = DiningStats(user=self.testUser)

        # Test voor 100%
        stats.total_participated = 10
        stats.total_helped = 10

        self.assertEqual(stats.get_percentage(), 100, "Percentage is not from 1 to 100")

        # Test voor 0%

        stats.total_helped = 0

        self.assertEqual(stats.get_percentage(), 0, "Percentage fails at 0")

        # Test voor minder als 5 keer meegeholpen

        stats.total_participated = 4

        self.assertEqual(stats.get_percentage(), 100, "Less then 5 times helping will not work")

        # test voor raar percentage

        stats.total_helped = 35
        stats.total_participated = 84

        self.assertEquals(stats.get_percentage(), 42)

    def test_new_participation(self):
        dlist = DiningList.get_latest()
        dlist.owner = self.testUser

        dlist.save()

        dpart = DiningParticipation(user=self.testUser, dining_list=dlist)

        dpart.work_cook = True

        dpart.save()

        dstats = DiningStats.objects.get(user=self.testUser)

        self.assertEquals(dstats.total_helped, 1)
        self.assertEquals(dstats.total_participated, 1)

        # Now we update

        dpart.work_cook = False

        dpart.save()

        dstats = DiningStats.objects.get(user=self.testUser)

        self.assertEqual(dstats.total_helped, 0)
        self.assertEqual(dstats.total_participated, 1)

        # Now we test for cooking and dishes at the same time

        dpart.work_cook = True
        dpart.work_dishes = True

        dpart.save()

        dstats = DiningStats.objects.get(user=self.testUser)

        self.assertEqual(dstats.total_helped, 1)
        self.assertEqual(dstats.total_participated, 1)


class DiningListTest(SimpleTestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("test", "test@test.com", "test")
        self.testUser.save()

    def tearDown(self):
        self.testUser.delete()

    def test_get_registered_user(self):
        dlist = DiningList().get_latest()

        dlist.save()

        dpart = DiningParticipation(user=self.testUser, dining_list=dlist)

        dpart.save()

        # Tests

        self.assertEqual(len(dlist.get_participants()), 1)

        dpart.delete()
        dlist.delete()

    def test_get_latest(self):
        dlist = DiningList.get_latest()

        self.assertEqual(dlist.relevant_date, datetime.now().date())

    def test_get_specific_date(self):
        date_user = datetime(2012, 11, 1)
        dlist = DiningList.get_specific_date(date_user.day, date_user.month, date_user.year)

        self.assertEqual(dlist.relevant_date, date_user)

        # Test that we cannot get dates from the future

        date_user = datetime(2050, 11, 1)
        dlist = DiningList.get_specific_date(date_user.day, date_user.month, date_user.year)

        self.assertEqual(dlist.relevant_date, datetime.now().date())


class ClaimViewTest(SimpleTestCase):
    view_url = reverse("dining:claim")

    def setUp(self):
        self.testUser = User.objects.create_user("test", "test@test.com", "test")
        self.testUser.save()

        self.testUser2 = User.objects.create_user("test2", "test@test.com", "test")
        self.testUser2.save()

    def tearDown(self):
        self.testUser.delete()
        self.testUser2.delete()

    def test_claim(self):
        dlist = DiningList.get_latest()
        dlist.save()

        self.client.login(username="test", password="test")

        # We test claiming the dining list without participation

        r = self.client.get(self.view_url)

        dlist = DiningList.get_latest()

        self.assertIsNone(dlist.owner)

        # We test claiming the dining list with a participation

        dpart = DiningParticipation(user=self.testUser, dining_list=dlist)
        dpart.save()

        self.assertIsNone(dlist.owner)

        r = self.client.get(self.view_url)

        self.assertEqual(r.status_code, 302)

        dlist = DiningList.get_latest()

        self.assertIsNotNone(dlist.owner)
        self.assertEqual(dlist.owner, self.testUser)

        # Test that you cannot claim a dining list over someone else

        dpart = DiningParticipation(user=self.testUser2, dining_list=dlist)

        dpart.save()

        self.client.login(username=self.testUser2.username, password="test")

        r = self.client.get(self.view_url)

        self.assertEqual(r.status_code, 302)

        dlist = DiningList.get_latest()

        self.assertNotEqual(dlist.owner, self.testUser2)
        self.assertEqual(dlist.owner, self.testUser)

        dpart.delete()
        dlist.delete()

    def test_cant_access_logged_out(self):
        r = self.client.get(self.view_url)

        self.assertEqual(r.status_code, 302)


class StatsViewTest(SimpleTestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("test", "test@test.com", "test")
        self.testUser.save()
        self.view_url = reverse("dining:stats")

    def tearDown(self):
        self.testUser.delete

    def test_login_only_superuser(self):
        self.client.login(username="test", password="test")

        r = self.client.get(self.view_url)

        self.assertEqual(r.status_code, 302)

        self.testUser.is_superuser = True

        self.testUser.save()

        r = self.client.get(self.view_url)

        self.assertEqual(r.status_code, 200)
