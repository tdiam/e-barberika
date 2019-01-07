from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker

from ..helpers import ApiResponse


class AR_SerializableUser(User):
    '''Proxy User model with __serialize__ method.

    A native Django model was needed, since declaring temporary models in Django tests is tricky.
    '''
    class Meta:
        proxy = True

    def __serialize__(self):
        return OrderedDict(
            first=self.first_name,
            last=self.last_name,
        )


class ApiResponseTestCase(TestCase):
    '''Unit test for the ApiResponse helper'''

    def setUp(self):
        # Use Faker to create 40 users
        fake = Faker('el_GR')
        names = [(fake.user_name(), fake.first_name(), fake.last_name()) for _ in range(40)]

        users = [AR_SerializableUser(username=u, first_name=f, last_name=l) for u, f, l in names]
        # Create in a single query
        AR_SerializableUser.objects.bulk_create(users)

    def test_single_instance_serialization(self):
        '''Check if serialization of a single user works correctly'''
        # Get one user
        user = AR_SerializableUser.objects.all()[0]
        response = ApiResponse(user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), f'{{"first": "{user.first_name}", "last": "{user.last_name}"}}')

    def test_complex_data_serialization(self):
        '''Use mixed data with normal Python objects and Django models'''
        users = AR_SerializableUser.objects.all()[:20]
        data = OrderedDict(
            start=0,
            count=20,
            users=users
        )
        response = ApiResponse(data)

        json_of_users = [f'{{"first": "{user.first_name}", "last": "{user.last_name}"}}' for user in users]
        json_of_users = ', '.join(json_of_users)
        json_of_users = '[' + json_of_users + ']'

        self.assertEqual(response.content.decode(), f'{{"start": 0, "count": 20, "users": {json_of_users}}}')
