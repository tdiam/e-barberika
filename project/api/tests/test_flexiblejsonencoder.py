import json
from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase

from ..helpers import FlexibleJsonEncoder


class FJE_SerializableUser(User):
    '''Proxy User model with __serialize__ method.

    A native Django model was needed to test __serialize__,
    since declaring temporary models in Django tests is tricky.
    '''
    class Meta:
        proxy = True

    def __serialize__(self, upper=False):
        first_name = self.first_name.upper() if upper else self.first_name
        last_name = self.last_name.upper() if upper else self.last_name

        return OrderedDict(
            name=OrderedDict(
                first=first_name,
                last=last_name
            ),
            username=self.username,
            email=self.email
        )

def _to_json(data, **kwargs):
    '''Helper function to convert data to JSON using the FlexibleJsonEncoder'''
    return json.dumps(data, cls=FlexibleJsonEncoder, ensure_ascii=False, **kwargs)


class FlexibleJsonEncoderTestCase(TestCase):
    '''Unit test for FlexibleJsonEncoder'''

    def setUp(self):
        # Create user
        self.user = FJE_SerializableUser(
            first_name='Γιώργος',
            last_name='Μαζωνάκης',
            username='gmazw',
            email='info@mazw.gr'
        )
        self.user.save()

        # Store expected representation for easy access
        self.instance_json = '{"name": {"first": "Γιώργος", "last": "Μαζωνάκης"}, "username": "gmazw", "email": "info@mazw.gr"}'
        # List and queryset representation
        self.list_json = f'[{self.instance_json}]'

    def test_instance_serialization(self):
        '''Check if serialization of a user instance works correctly'''
        res = _to_json(self.user)
        self.assertEqual(res, self.instance_json)

    def test_serialize_args(self):
        '''serialize_args in json.dumps must be passed as arguments to the __serialize__ method'''
        res = _to_json(self.user, serialize_args={'upper': True})
        self.assertEqual(res, '{"name": {"first": "ΓΙΏΡΓΟΣ", "last": "ΜΑΖΩΝΆΚΗΣ"}, "username": "gmazw", "email": "info@mazw.gr"}')

    def test_extra_serialize_args_do_not_raise_exception(self):
        '''Check if only the defined arguments of __serialize__ are passed'''
        # If not, this should raise a TypeError
        _res = _to_json(self.user, serialize_args={'non_existent_arg': 'random value'})

    def test_list_serialization(self):
        '''Check if serialization of a user list works correctly'''
        res = _to_json([self.user])
        self.assertEqual(res, self.list_json)

    def test_queryset_serialization(self):
        '''Check if serialization of a user queryset works correctly'''
        res = _to_json(FJE_SerializableUser.objects.all())
        self.assertEqual(res, self.list_json)

    def test_user_is_not_serializable(self):
        '''Native User model has no __serialize__ so an exception should be raised from json.dumps'''
        native_user = User(username='test')
        with self.assertRaises(TypeError):
            _res = _to_json(native_user)
