from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from online_users.models import OnlineUserActivity


class OnlineUserMiddlewareTest(TestCase):

    @staticmethod
    def get_active_user_count():
        last_hour = timedelta(minutes=60)
        return OnlineUserActivity.get_user_activities(last_hour).count()

    def create_and_login_user(self):
        password = 'test1!'
        user = User.objects.create_user(username='testUser1', email='test@test.com', password=password)
        self.client.login(username=user.username, password=password)

    def url_request(self, url):
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        return response

    def test_anonymous_user_not_added(self):
        self.url_request('')
        self.assertEqual(self.get_active_user_count(), 0)

    def test_user_added_and_updated(self):
        self.create_and_login_user()
        for i in range(3):
            self.url_request('')
            self.assertEqual(self.get_active_user_count(), 1)
