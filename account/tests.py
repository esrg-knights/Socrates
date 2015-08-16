from django.contrib.auth.models import User
from django.test import SimpleTestCase, Client

from .forms import LoginForm

# Create your tests here.
class ModelTests(SimpleTestCase):
    pass

class ViewTests(SimpleTestCase):
    @classmethod
    def setUp(self):
        self.client = Client
        test_user = User.objects.get_or_create(username='test', password='test', email="test@test.com", is_staff=False, is_superuser=False)

    def test_can_login(self):
        response = self.client.post('/account/login/', {"username":"test", "password":"test"}, follow=True)

        self.assertEqual(response.status_code, 200)