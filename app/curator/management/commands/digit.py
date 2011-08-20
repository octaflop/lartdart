from django.core.management.base import BaseCommand, CommandError
from curator.utils import *
from settings import UUID
import urllib2 as urllib
import simplejson as json
from pprint import pprint

class Command(BaseCommand):
    args = '<location>'
    help = 'Snags the latest information about local art shows based on the\
        location.'
    def handle(self, *args, **options):
        location = args[0]
        ##print yellowfinds(location)
        pprint(get_yellow_json(location))
        crunchit(location)
        #feedfinds(location)
        return
