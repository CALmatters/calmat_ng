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

        src_field = options['src']
        dst_field = options['dst']
        app_name, model_name = options['model'].split(':')

        Model = apps.get_model(app_name, model_name)

        for obj in Model.objects.all():
            print("Processing {}".format(obj.title))

            try:
                src_path_rel = getattr(obj, src_field).path
            except ValueError:
                print("No image for '{}' on {} {}".format(
                    src_field, model_name, obj.title))
            else:
                src_path_abs = os.path.join(settings.MEDIA_ROOT, src_path_rel)

                fname = src_path_abs.split('/')[-1]
                to_path_rel = os.path.join('uploads/', fname)
                to_path_abs = os.path.join(settings.MEDIA_ROOT, to_path_rel)

                print(src_path_abs, to_path_rel, to_path_abs)
                try:
                    shutil.move(src_path_abs, to_path_abs)
                except FileNotFoundError:
                    pass

                default_caption = '{} {} image'.format(obj.title, model_name)
                defaults = dict(
                    caption=default_caption, alt_tag=default_caption)

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



