from django.conf import settings
from django.http import HttpRequest


class MediaHttpRequest(HttpRequest):
    def __init__(self):
        super().__init__()

        self.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }


class BasketTestMixin:
    def set_up_basket_session(self, basket_id):
        session = self.client.session
        session[settings.BASKET_SESSION_ID] = basket_id
        session.save()
