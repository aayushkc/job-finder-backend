from django.db import models

# Create your models here.
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from wagtail.search import index

from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    # api_fields = [
    #     APIField('body'),
    #     APIField('intro'),
    # ]


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    thumbnail = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True,blank=True)
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('thumbnail'),
    ]

    api_fields = [
        APIField('body'),
        APIField('intro'),
        APIField('thumbnail', serializer=ImageRenditionField('height-165')),
    ]