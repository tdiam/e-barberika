from django.test import TestCase

from ..helpers import ApiMessage

class ApiMessageTestCase(TestCase):
    '''Unit test for the ApiMessage helper'''

    def test_message_ok(self):
        '''Simple message check'''
        response = ApiMessage('OK')
        self.assertEqual(response.content.decode(), '{"message": "OK"}')

    def test_utf8_characters(self):
        '''Check that UTF-8 characters are not escaped'''
        response = ApiMessage('Το παπάκι πάει στην ποταμιά')
        self.assertEqual(response.content.decode(), '{"message": "Το παπάκι πάει στην ποταμιά"}')

    def test_kwargs_work(self):
        '''Check if kwargs are passed to JsonResponse correctly'''
        response = ApiMessage('Unauthorized', status=401)
        self.assertEqual(response.status_code, 401)
