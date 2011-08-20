import urllib2 as urllib
import simplejson as json
from settings import UUID
from django.db import models
from curator.models import Event, Artist, Gallery, Location

# TODO: put these in settings
##YELLOW_ROOT = "http://api.yellowapi.com"
YELLOW_ROOT = "http://api.sandbox.yellowapi.com"
YELLOWAPIKEY = "ytkandhaz2mwjhkp58wwgw8a"

def get_yellow_json(location):
    '''
    returns json results from the api call
    '''
    sflags = ''
    paramtemp = "/FindBusiness/?what=%(what)s&where=%(where)s&fmt=json&sflag=%(flags)s&apikey=%(apikey)s&UID=%(uid)s" % {
        'what': "art-gallery",
        'where': location,
        'apikey': YELLOWAPIKEY,
        'uid': UUID,
        'flags': sflags,
        }
    url = "%s%s" % (YELLOW_ROOT, paramtemp)
    print "Snagging results from yellow api on url:\n %s" % url
    req = urllib.Request(url)
    ret = json.loads(urllib.urlopen(req).read())
    return ret

def crunchit(location):
    '''
    a static function which writes to the model
    '''
    results = get_yellow_json(location)
    count = 0
    for res in results['listings']:
        ##try:
         #   gallery = Gallery.objects.get(res['name'])
        ##except models.ObjectDoesNotExist:
        gallery = Gallery()
        lat = res['geoCode']['latitude']
        lng = res['geoCode']['longitude']
        add = ""
        for ad in res['address'].values():
            add += " %s" % ad
        location = Location(place=add, lat=lat, lng=lng)
        location.save()
        gallery.name = res['name']
        gallery.ypwebsite = res['merchantUrl']
        gallery.location = location
        count += 1
        try:
            gallery.save()
            ret = "%i entries saves" % count
        except:
            ret = 'there was an error saving the gallery'
    return ret


