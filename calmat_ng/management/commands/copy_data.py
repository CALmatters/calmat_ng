from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('from_table')
        parser.add_argument('from_fields')
        parser.add_argument('to_table')
        parser.add_argument('to_fields')

    def handle(self, *args, **options):

        print(options)

        from_table = options['from_table']
        from_fields = options['from_fields']
        to_table = options['to_table']
        to_fields = options['to_fields']


