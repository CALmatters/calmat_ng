import shutil
import os
from django.core.management import BaseCommand
from django.apps import apps
from django.conf import settings

from media_manager.models import MediaItem


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument('src')
        parser.add_argument('dst')
        parser.add_argument('model')

    def handle(self, *args, **options):

        print(options)

        src_field = options['src']
        dst_field = options['dst']
        app_name, model_name = options['model'].split(':')

        Model = apps.get_model(app_name, model_name)

        for obj in Model.objects.all():
            from_path = os.path.join(
                settings.MEDIA_ROOT, getattr(obj, src_field).path)
            fname = from_path.split('/')[-1]
            to_path_rel = os.path.join('uploads/', fname)
            to_path = os.path.join(settings.MEDIA_ROOT, to_path_rel)

            print(from_path, to_path_rel, to_path)
            try:
                shutil.move(from_path, to_path)
            except FileNotFoundError:
                pass

            default_caption = '{} {} image'.format(obj.title, model_name)
            defaults = dict(caption=default_caption, alt_tag=default_caption)

            item, created = MediaItem.objects.get_or_create(
                file=to_path_rel, defaults=defaults)
            print(created, item)

            if not created:
                item.caption = default_caption
                item.alt_tag = default_caption
                item.save()

            if getattr(obj, dst_field) != item:
                setattr(obj, dst_field, item)
                obj.save()



