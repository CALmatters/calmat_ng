import re
from html.entities import name2codepoint

from django import template
from django.utils.html import escape, strip_tags

register = template.Library()


def decode_entities(html):
    """
    Remove HTML entities from a string.
    Adapted from http://effbot.org/zone/re-sub.htm#unescape-html
    Stolen from Mezzanine
    """
    def decode(m):
        html = m.group(0)
        if html[:2] == "&#":
            try:
                if html[:3] == "&#x":
                    return chr(int(html[3:-1], 16))
                else:
                    return chr(int(html[2:-1]))
            except ValueError:
                pass
        else:
            try:
                html = chr(name2codepoint[html[1:-1]])
            except KeyError:
                pass
        return html
    return re.sub("&#?\w+;", decode, html.replace("&amp;", "&"))


@register.simple_tag
def metablock(parsed):
    """
    Remove HTML tags, entities and superfluous characters from
    meta blocks.
    Stolen from Mezzanine
    """

    parsed = " ".join(parsed.replace("\n", "").split()).replace(" ,", ",")
    return escape(strip_tags(decode_entities(parsed)))
