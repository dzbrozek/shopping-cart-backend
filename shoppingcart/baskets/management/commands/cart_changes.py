from baskets.models import Basket
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from users.models import User


class Command(BaseCommand):
    help = "Command sending to admins list of baskets that changed since the last check"

    def handle(self, *args, **options):
        baskets = Basket.objects.filter(updated=True)
        admins = User.objects.filter(is_admin=True, is_active=True)

        num_baskets = baskets.count()
        if not num_baskets:
            self.stderr.write('Found 0 changed baskets')
            return
        if not admins.exists():
            self.stderr.write('Found 0 admins')
            return

        message = render_to_string('baskets/baskets_changes.txt', {'baskets': baskets})
        send_mail(
            'Changed baskets', message, settings.DEFAULT_FROM_EMAIL, list(admins.values_list('email', flat=True)),
        )

        baskets.update(updated=False)

        self.stdout.write('Sent email with %s changed baskets.' % num_baskets)
