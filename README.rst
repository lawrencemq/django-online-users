django-online-users
===================

Tracks the time of each user's last action

Using middleware, django-online-users will keep track of each user and the timestamp of their last action in the database.

Admins can see this data in the admin portal, and the database can be queried using timedeltas.

This is meant for smaller applications as each HTTP request will result in a database entry update.

Requirements
------------

- Python: 2.7, 3.3, 3.4, 3.5, 3.6
- Django: 1.11+


Setup
-----------

1. Add "online_users" to your ``INSTALLED_APPS``


.. code-block:: python

    INSTALLED_APPS = [
        ...
        'online_users',
    ]


2. Add the ``OnlineNowMiddleware`` to your ``MIDDLEWARE_CLASSES`` after the ``SessionMiddleware``


.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'online_users.middleware.OnlineNowMiddleware',
    )


3. Run ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the tables in the database.


Rollout
-------

If this application is intended to be used in an application already in production, it's recommended that the middleware
be added to the settings file *after* the application has been installed and the database has been migrated. Otherwise,
HTTP requests may result in a 500 error.


Use
---

* The time of the last action for each user can be seen in the admin portal at http://127.0.0.1:8000/admin/online_users/onlineuser/


* To retrieve the current number of users online in the last 15 minutes


.. code-block:: python

    from datetime import timedelta
    ...
    user_activity_objects = OnlineUserActivity.get_user_activities()
    number_of_active_users = user_activity_objects.count()


* A timedelta can also be specified to the ``get_user_activities()`` with to find activity


.. code-block:: python

    from datetime import timedelta
    ...
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=60)
    users = (user for user in user_activity_objects)


API
---

OnlineUserActivity holds two values: `user`, the user in question, and `last_activity`, a timestamp stored as a DateTimeField.

``OnlineUserActivity.get_user_activities()`` will return OnlineUserActivity objects for the last 15 minutes by default.
Developers can also pass in a time delta of a different length of time for the query. The response is a QuerySet containing
the active users during that time period, and the items are sorted in descending chronological order.


Change Log
------------

* 0.3 - Updating to have on_delete = models.CASCADE
* 0.2 - Updating to Django 1.11. Changed from basic User model to settings.AUTH_USER_MODEL.