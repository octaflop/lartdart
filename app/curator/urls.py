from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
    url('^$', home_view, name='home_view'),
    url('^gallery/(?P<slug>[\w\-]+)', gallery_object_view, name='gallery_object_view'),
#    url(r'/r/^(?P<region>[\w\-]+)', region_index_view, name='location_view'),

#    url(r'^artist/(?P<slug>[\w\-]+)', member_detail_view, name='artist_view'),
#    url(r'^event/(?P<slug>[\w\-]+)', member_detail_view, name='event_view'),
)

