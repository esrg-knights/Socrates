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


class RegistrationTest(SimpleTestCase):
    def test_can_register(self):
        response = self.client.post("/account/register/",
                                    {'email': "test@test.com", 'username': 'test2', 'password': 'test',
                                     'password_repeat': 'test', 'first_name': 'test', 'last_name': 'test'})

        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(username="test2")
        self.assertIsNotNone(new_user, "No new user was created")
        self.assertFalse(new_user.is_active, "New user is active while it should not be")

        new_user.delete()

    def test_passwords_do_not_match(self):
        response = self.client.post("/account/register/",
                                    {'email': "test@test.com", 'username': 'test2', 'password': 'not-test',
                                     'password_repeat': 'test', 'first_name': 'test', 'last_name': 'test'})

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(User.objects.filter(username='test2'))


class ActivationTest(SimpleTestCase):
    def setUp(self):
        response = self.client.post("/account/register/",
                                    {'email': "test@test.com", 'username': 'test', 'password': 'test',
                                     'password_repeat': 'test', 'first_name': 'test', 'last_name': 'test'})

        self.user = User.objects.get(username='test')

        self.activation_url = "/account/activate/{0}/".format(self.user.id)

    def tearDown(self):
        self.user.delete()

    def test_activation(self):
        response = self.client.get(self.activation_url, {})

        self.assertEqual(response.status_code, 200, "Correct page not found")
