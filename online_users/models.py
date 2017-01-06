from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class OnlineUserActivity(models.Model):
    user = models.OneToOneField(User)
    last_activity = models.DateTimeField()

    @staticmethod
    def update_user_activity(user):
        OnlineUserActivity.objects.update_or_create(user=user, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=15)):
        starting_time = timezone.now() - time_delta
        return OnlineUserActivity.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')
