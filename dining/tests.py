# Create your tests here.
from django.contrib.auth.models import User
from django.test import SimpleTestCase

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

    def test_new_participation(self):
        dlist = DiningList(started_by=self.testUser, owner=self.testUser)

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
        self.testUser = User.objects.create_user("test", "test", "test@test.com")
        self.testUser.save()

    def tearDown(self):
        self.testUser.delete()

    def test_get_registered_user(self):
        dlist = DiningList(started_by=self.testUser)

        dlist.save()

        dpart = DiningParticipation(user=self.testUser, dining_list=dlist)

        dpart.save()

        # Tests

        self.assertEqual(len(dlist.get_participants()), 1)
