from online_users.models import OnlineUserActivity


class OnlineNowMiddleware(object):
    """Updates the OnlineUserActivity database whenever an authenticated user makes an HTTP request."""

    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated():
            return

        OnlineUserActivity.update_user_activity(user)
