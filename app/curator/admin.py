from django.contrib import admin

from curator.models import Gallery, Event, Artist

class GalleryAdmin(admin.ModelAdmin):
    pass

class GalleryAdmin(admin.ModelAdmin):
    pass

class GalleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Artist, ArtistAdmin)
