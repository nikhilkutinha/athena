from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
import requests

import json
import csv

from reports.models import Region

BASE_DIR = settings.BASE_DIR
BLACKLIST = ['Unknown']

class Command(BaseCommand):
    help = 'Inserts regions into the database.'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', type=str)

    def handle(self, *args, **options):
        for line in self.get_dataset():
            uid = line.get('UID')
            iso = line.get('iso2')
            latitude = line.get('Lat') or None
            longitude = line.get('Long_') or None
            country = line.get('Country_Region')
            province = line.get('Province_State')
            name = province or country

            if province:
                zone = Region.PROVINCE
            elif country:
                zone = Region.COUNTRY

            if name not in BLACKLIST:
                defaults = {
                    'pk': uid,
                    'name': name,
                    'iso': iso,
                    'latitude': latitude,
                    'longitude': longitude,
                    'type': zone,
                }

                region, _ = Region.objects.update_or_create(pk=uid, defaults=defaults)

                if country and zone is Region.PROVINCE:
                    country = Region.objects.get(name=country, type=Region.COUNTRY)
                    region.parent = country

                region.save()

    def get_dataset(self, **options):
        if 'file' in options:
            return self.get_dataset_from_file(options['file'][0])

        else:
            return self.get_dataset_from_github()

    def get_dataset_from_file(self, path):
        with open(path) as f:
            return csv.DictReader(f)

    def get_dataset_from_github(self):
        with open(BASE_DIR / 'files/urls.json') as f:
            urls = json.load(f)

        res = requests.get(urls['regions'])
        content = res.content.decode('utf-8')
        return csv.DictReader(content.splitlines(), delimiter=',')
