import csv
import datetime

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.db import connection

DISTRIBUTIONS_2016_SQL = """
SELECT distinct a.title, c.title AS publisher, f.title AS owner,
a.publish_date, b.date_published, u.username
FROM business_partnerarticle b
FULL OUTER JOIN pages_article a ON b.article_id=a.id
FULL OUTER JOIN business_partner c ON b.partner_id=c.id
FULL OUTER JOIN pages_article_authors d ON a.id=d.article_id
FULL OUTER JOIN business_person e ON d.person_id = e.id
FULL OUTER JOIN auth_user u ON e.user_id = u.id
FULL OUTER JOIN business_partnerowner f ON c.owner_id = f.id
WHERE a.publish_date > '2016-01-01'
AND b.fulltext_or_mention = 'Full Text Publish'
ORDER by a.publish_date;"""


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

    @staticmethod
    def yield_distribution_rows(year='2016'):
        cursor = connection.cursor()

        cursor.execute(DISTRIBUTIONS_2016_SQL)

        for row in cursor.fetchall():
            yield row

    def export_2016_distrubutions(modeladmin, request, queryset):

        if not request.user.is_staff:
            raise PermissionDenied

        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        file_name = "%s_%s" % (
            opts.verbose_name.lower(), datetime.datetime.now())
        response[
            'Content-Disposition'] = 'attachment; filename=%s.csv' % file_name
        writer = csv.writer(response)

        for row in AdminCSVExport.yield_distribution_rows():
            writer.writerow(row)
        return response

    export_2016_distrubutions.short_description = "Export 2016 distributions"

    actions = [export_as_csv, export_2016_distrubutions]