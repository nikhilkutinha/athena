from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django.conf import settings
import requests

import json
import csv
import os

from ... models import Region, Report


BASE_DIR = settings.BASE_DIR

COUNTRY = Region.COUNTRY
PROVINCE = Region.PROVINCE

BLACKLIST = ['Unknown']         # HACK
CRUSE_SHIPS = [
    'Diamond Princess',         # HACK
    'Grand Princess'
]

class Command(BaseCommand):
    help = 'Inserts regions into the database.'

    def add_arguments(self, parser):
        parser.add_argument('from-file', nargs='?', type=str)

    def get_dataset(self, **options):
        
        if "from-file" in options:
            path = options['from-file'][0]
            with open(path) as f:
                dataset = csv.reader(f)

        else:
            with open(BASE_DIR / "files/urls.json") as f:
                urls = json.load(f)

            res = requests.get(urls["regions"])
            text = res.content.decode('utf-8')
            dataset = csv.reader(text.splitlines(), delimiter=',')

        return dataset
       

    def handle(self, *args, **options):

        dataset = self.get_dataset()

        # skip csv headers
        next(dataset)

        for line in dataset:

            uid = line[0]
            iso = line[1]
            latitude = line[8] or None
            longitude = line[9] or None

            country = line[7]
            province = line[6]

            name = province or country
            flag = ""

            if province:
                zone = PROVINCE
            elif country:
                zone = COUNTRY

            # zone is COUNTRY if name in CRUSE_SHIPS else zone

            if iso and zone is COUNTRY:
                try:
                    filename = iso.lower() + '.svg'
                    img = BASE_DIR / 'files/flags' / filename
                    flag = File(open(img, 'rb'))

                except FileNotFoundError:
                    pass

            if name not in BLACKLIST:

                defaults = {
                    'pk': uid, 
                    'name': name, 
                    'iso': iso,
                    'latitude': latitude, 
                    'longitude': longitude,
                    'type': zone
                }

                region, _ = Region.objects.update_or_create(pk=uid,
                                                            defaults=defaults)

                if zone is PROVINCE and country is not None:
                    country = Region.objects.get(name=country,
                                                 type=COUNTRY)
                    region.parent = country

                # upload flag image if available
                if flag:
                    region.flag.save(filename, flag)

                region.save()
