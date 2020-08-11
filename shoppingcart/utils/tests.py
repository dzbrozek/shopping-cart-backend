from django.http import HttpRequest


class MediaHttpRequest(HttpRequest):
    def __init__(self):
        super().__init__()

        self.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
