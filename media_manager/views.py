from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from media_manager.models import MediaItem


def media_lookup(request, media_id):

    mi = MediaItem.objects.get(pk=media_id)

    item_dict = dict(id=mi.id, desc=mi.caption, credit=mi.creator)

    return JsonResponse(item_dict)
