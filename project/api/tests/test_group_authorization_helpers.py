from django.test import TestCase
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .helpers import ApiRequestFactory
from ..helpers import is_volunteer, is_admin, volunteer_required, admin_required


User = get_user_model()
OK_RESPONSE = HttpResponse('OK')

def normal_view_func(_req):
    return OK_RESPONSE

@volunteer_required
def view_func_for_volunteers(_req):
    return OK_RESPONSE

@admin_required
def view_func_for_admins(_req):
    return OK_RESPONSE

class NormalClassView(View):
    def get(self, request):
        return OK_RESPONSE

class VolunteerClassView(View):
    @method_decorator(volunteer_required)
    def get(self, request):
        return OK_RESPONSE

class AdminClassView(View):
    @method_decorator(admin_required)
    def get(self, request):
        return OK_RESPONSE


class GroupAuthorizationHelpersTestCase(TestCase):
    def setUp(self):
        anon = AnonymousUser()
        volunteer = User.objects.create_user(username='volunteer', password='volunteer')
        # Create Volunteer group since this will be executed in a test database
        volunteer.groups.create(name='Volunteer')
        admin = User.objects.create_user(username='admin', password='admin', is_staff=True)

        # User information for easy access
        self.users = [{
            'title': 'Anonymous user',
            'user': anon,
            'is_volunteer': False,
            'is_admin': False,
        }, {
            'title': 'Volunteer',
            'user': volunteer,
            'is_volunteer': True,
            'is_admin': False,
        }, {
            'title': 'Admin',
            'user': admin,
            'is_volunteer': True,
            'is_admin': True,
        }]

        # Generate a request for each user
        for user in self.users:
            user['req'] = ApiRequestFactory().get('/')
            user['req'].user = user['user']

    def test_is_volunteer(self):
        '''Unit test for the `is_volunteer` helper'''
        for user in self.users:
            with self.subTest(msg=user['title']):
                self.assertEqual(is_volunteer(user['req']), user['is_volunteer'])

    def test_is_admin(self):
        '''Unit test for the `is_admin` helper'''
        for user in self.users:
            with self.subTest(msg=user['title']):
                self.assertEqual(is_admin(user['req']), user['is_admin'])

    def test_normal_view_function(self):
        '''Check if all users can access normal view function'''
        view = normal_view_func

        for user in self.users:
            with self.subTest(msg=user['title']):
                res = view(user['req'])
                self.assertEqual(res.status_code, 200)

    def test_normal_class_view(self):
        '''Check if all users can access normal class based view'''
        view = NormalClassView.as_view()

        for user in self.users:
            with self.subTest(msg=user['title']):
                res = view(user['req'])
                self.assertEqual(res.status_code, 200)

    def test_volunteer_view_function(self):
        '''Check if only users with Volunteer permissions can access volunteer view function'''
        view = view_func_for_volunteers

        for user in self.users:
            with self.subTest(msg=user['title']):
                res = view(user['req'])
                self.assertEqual(res.status_code, 200 if user['is_volunteer'] else 401)

    def test_volunteer_class_view(self):
        '''Check if only users with Volunteer permissions can access volunteer class based view'''
        view = VolunteerClassView.as_view()

        for user in self.users:
            with self.subTest(msg=user['title']):
                res = view(user['req'])
                self.assertEqual(res.status_code, 200 if user['is_volunteer'] else 401)

    def test_admin_view_function(self):
        '''Check if only users with Admin permissions can access admin view function'''
        view = view_func_for_admins

        for user in self.users:
            with self.subTest(msg=user['title']):
                res = view(user['req'])
                self.assertEqual(res.status_code, 200 if user['is_admin'] else 401)

    def test_admin_class_view(self):
        '''Check if only users with Admin permissions can access admin class based view'''
        view = AdminClassView.as_view()

        for user in self.users:
            with self.subTest(msg=user['title']):
                res = view(user['req'])
                self.assertEqual(res.status_code, 200 if user['is_admin'] else 401)
