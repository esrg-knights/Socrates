from django.contrib.auth.models import User
from django.test import SimpleTestCase, Client

# Create your tests here.

def create_test_user():
    t = User.objects._create_user(username="test", password="test", email="test", is_staff=False,
                                  is_superuser=False)


def delete_test_user():
    User.objects.get(username="test").delete()


class LogoutTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        create_test_user()

    def tearDown(self):
        delete_test_user()

    def test_logout(self):
        self.client.login(username="test", password="test")

        response = self.client.get("/account/logout/")

        self.assertEqual(response.status_code, 302)

class LoginTests(SimpleTestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        create_test_user()

    def tearDown(self):
        User.objects.get(username="test").delete()

    def test_can_login(self):
        response = self.client.post('/account/login/', {"username": "test", "password": "test"})

        self.assertEqual(response.status_code, 302, "User was not redirected on succesfull login")

    def test_wrong_password_fails(self):
        response = self.client.post('/account/login/', {"username": "test", "password": "will fail"})

        self.assertEqual(response.status_code, 200, "Server failed")

        messages = response.context['messages']._loaded_data[0]

        self.assertEqual(messages.level, 30)

    def test_inactive_user(self):
        inactive = User.objects.create_user(username="test2", password="test", email="test@test.com")

        inactive.is_active = False
        inactive.save()

        response = self.client.post('/account/login/', {"username": "test2", "password": "test"})

        self.assertEqual(response.status_code, 200)

        messages = response.context['messages']._loaded_data[0]

        self.assertEqual(messages.level, 40, "Login message did nto have the correct level")

        inactive.delete()
