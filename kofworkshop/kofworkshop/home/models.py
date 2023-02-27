from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    post = RichTextField(blank=True)

    for item in post:
        pass
    content_panels = Page.content_panels + [
        FieldPanel('post', classname='full')
    ]
