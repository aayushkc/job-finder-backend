from django.db import models

# Create your models here.
from wagtail import blocks

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
# from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField

from wagtail.images.blocks import ImageChooserBlock as DefaultImageChooserBlock

class ImageChooserBlock(DefaultImageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value:
            return {
                'id': value.id,
                'title': value.title,
                'large': value.get_rendition('width-1000').attrs_dict,
            }
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    preview_modes = []

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title",required=False)),
        ('paragraph', blocks.RichTextBlock(required=False)),
        ('image', ImageChooserBlock(required=False)),
    ], blank=True)
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

    preview_modes = []
