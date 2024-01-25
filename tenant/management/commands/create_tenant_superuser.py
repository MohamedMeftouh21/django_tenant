from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser for the specified tenant'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Superuser email')
        parser.add_argument('first_name', type=str, help='Superuser first_name')
        parser.add_argument('last_name', type=str, help='Superuser last_name')

        parser.add_argument('password', type=str, help='Superuser password')

    def handle(self, *args, **options):
        superuser_email = options['email']
        superuser_first_name = options['first_name']
        superuser_last_name = options['last_name']

        superuser_password = options['password']

        tenant_schema_name = None
        if 'TENANT_SCHEMA_NAME' in options:
            tenant_schema_name = options['TENANT_SCHEMA_NAME']

        if not tenant_schema_name:
            self.stderr.write(self.style.ERROR('Tenant schema name is not provided.'))
            return

        with schema_context(tenant_schema_name):
            try:
                User.objects.create_superuser(
                    email=superuser_email,
                    first_name=superuser_first_name,
                    last_name=superuser_last_name,

                    password=superuser_password,
                )
                self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error creating superuser: {e}'))
                return
