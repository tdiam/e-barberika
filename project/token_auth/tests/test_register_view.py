from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from ..views import RegisterView


User = get_user_model()

class TokenAuthRegisterViewTestCase(TestCase):
    '''Checks the functionality of the RegisterView'''

    def setUp(self):
        # Create user
        self.username = 'johndoe'
        self.password = 'johndoe'
        User.objects.create_user(self.username, password=self.password)

        self.factory = RequestFactory()
        self.view = RegisterView.as_view()

    def test_missing_fields_should_fail(self):
        '''Registration without username or password should fail'''
        # Register without password
        request = self.factory.post('/', {
            'username': 'mattmurdock'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

        # Register without username
        request = self.factory.post('/', {
            'password': 'definitely blind'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_cant_create_user_with_same_username(self):
        '''Registration with existing username should fail'''
        request = self.factory.post('/', {
            'username': self.username,
            'password': 'whatever'
        })

        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_can_register_user(self):
        '''Registration with new username should succeed'''
        request = self.factory.post('/', {
            'username': 'mattmurdock',
            'password': 'definitely blind'
        })

        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='mattmurdock').exists())
