import csv

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


class AdminCSVExport(object):

    def export_as_csv(modeladmin, request, queryset):

        if not request.user.is_staff:
            raise PermissionDenied

        opts = modeladmin.model._meta
        response = HttpResponse( content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename=%s.csv' % opts.verbose_name
        writer = csv.writer(response)
        field_names = [field.name for field in opts.fields]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export selected objects as csv file"

    actions = [export_as_csv, ]