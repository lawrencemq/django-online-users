from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from online_users.models import OnlineUserActivity


class OnlineUserActivityTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='testUser1')
        self.user2 = User.objects.create(username='testUser2')
        self.time = timezone.now()
        self.time_five_min_ago = self.time - timedelta(minutes=5)
        self.online_user1 = OnlineUserActivity.objects.create(user=self.user1, last_activity=self.time)
        self.online_user2 = OnlineUserActivity.objects.create(user=self.user2, last_activity=self.time_five_min_ago)

    def test_update_activity_for_user(self):
        self.assertEqual(OnlineUserActivity.objects.all().count(), 2)
        OnlineUserActivity.update_user_activity(self.user1)
        self.assertEqual(OnlineUserActivity.objects.all().count(), 2)

    def test_get_active_users(self):
        online_users = OnlineUserActivity.get_user_activities(timedelta(minutes=6))
        self.assertEqual(online_users.count(), 2)

    def test_get_active_users__users_out_of_timedelta(self):
        online_users = OnlineUserActivity.get_user_activities(timedelta(minutes=1))
        self.assertEqual(online_users.count(), 1)

    def test_get_active_users_ordering(self):
        online_users = OnlineUserActivity.get_user_activities(timedelta(minutes=60))
        self.assertEqual(online_users.count(), 2)
        self.assertEqual(list(online_users), [self.online_user1, self.online_user2])
