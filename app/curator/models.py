from django.db import models
from curator.urlutils import unique_slugify
from django.template.defaultfilters import slugify

class Location(models.Model):
    """
    A basic location model
    """
    place = models.CharField("Place", max_length=250)
    lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True,
            null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=7, blank=True,
            null=True)

    def __unicode__(self):
        self.place

class Gallery(models.Model):
    """
    A gallery is a brick-and-morter representation
    """
    name = models.CharField("Name", help_text='the name of the art gallery',
        max_length=80)
    slug = models.SlugField(max_length=80)
    website = models.URLField("Website", blank=True, null=True)
    ypwebsite = models.URLField("Yellow Pages Website Listing")

    location = models.ForeignKey("Location", related_name="gallery-location")
    ##        blank=True, null=True)

    events = models.ForeignKey("Event", related_name="gallery-events", null=True,
        blank=True)
    artists = models.ForeignKey("Artist", related_name="gallery-artists", null=True,
        blank=True)

    def save(self, *args, **kwargs):
        slugstr = self.name
        ##unique_slugify(self, slugstr)
        slugify(slugstr)
        super(Gallery, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "gallery"
        verbose_name_plural = "galleries"

class Event(models.Model):
    """
    Events are any time-sensitive happenings
    """
    title = models.CharField("Title", max_length=80)
    slug = models.SlugField("Slug", max_length=80)
    when = models.DateTimeField("When")
    where = models.CharField("Where", max_length=180)
    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

class Artist(models.Model):
    name = models.CharField("Artist Name", max_length=180)
    slug = models.SlugField("Slug", max_length=80)
    genre = models.CharField("Genre", max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "artist"
        verbose_name_plural = "artists"

