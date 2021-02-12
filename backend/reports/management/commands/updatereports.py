from django.core.management.base import BaseCommand, CommandError
from ... models import Region, Report
from django.conf import settings
from django.shortcuts import get_object_or_404

import json
import csv
import os
import requests
from datetime import datetime

COUNTRY = Region.COUNTRY
PROVINCE = Region.COUNTRY
BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):

    help = 'Inserts reports into the database.'

    def add_arguments(self, parser):
        parser.add_argument('from-files', action='store_false')
        parser.add_argument('confirmed', nargs='?', type=str)
        parser.add_argument('deaths', nargs='?', type=str)
        parser.add_argument('recovered', nargs='?', type=str)

    @classmethod
    def format_date(cls, date):
        return datetime.strptime(date, '%m/%d/%y').date().__str__()

    @classmethod
    def extract_timeline(cls, dataset):
        """
        Normalize dataset into a format that can be seamlessly
        inserted into the database.

        Args:
            dataset: (required) Simply provide the output 
                from csv.reader()

        Returns:
            A dict representation of the parsed dataset.
        """

        global dates

        header = next(dataset)
        dates = [
            cls.format_date(date)
            for date in header[4:]
        ]
        timeline = {}

        for line in dataset:
            province, country, latitude, longitude, *counts = line
            timeline[country] = timeline.get(country, {})

            for index, date in enumerate(dates):
                timeline[country][date] = timeline[country].get(date, 0)
                timeline[country][date] += int(counts[index])

        return timeline

    def get_datasets(self, *args, **options):
        """
        Get datasets from filepaths if they were passed in via
        arguments else grab them from github. 

        Args:
            None

        Returns:
            A dict representation containing various datasets.
        """

        datasets = {}
        timelines = ["confirmed", "deaths", "recovered"]

        if "from_files" in options:
            for val in timelines:
                with open(options[val]) as f:
                    csv_file = csv.reader(f)
                datasets[val] = csv_file

        else:
            self.stdout.write(self.style.WARNING("You did not provide files to parse, "
                                                 "hence we'll be using datasets available "
                                                 "at github.com/cssegisanddata"))

            with open(BASE_DIR / 'files/urls.json') as f:
                urls = json.load(f)['urls']

            for val in timelines:
                res = requests.get(urls[val])
                text = res.content.decode('utf-8')
                datasets[val] = csv.reader(text.splitlines(), delimiter=',')

        return datasets

    def add_to_database(self, **kwargs):
        """
        Updates or creates report for a specific region/country.

        Args:
            confirmed: (required) Number of confirmed cases.
            deaths: (required) Number of deaths.
            recovered: (required) Number of recovered cases.
            date: (required) Date of the report in the following 
                format, YYYY-MM-DD.
            region: (required) Which region does this report 
                belong to.

        Returns:
            A tuple representation of the report object and
            a boolean depecting if the report was created.

            True = created
            False = updated.
        """

        region = Region.objects.get(name=kwargs["region"],
                                    type=COUNTRY)
        kwargs["region"] = region
        date = kwargs["date"]

        report, created = Report.objects.update_or_create(
            region=region,
            date=date,
            defaults=kwargs
        )

        return report, created

    def handle(self, *args, **options):

        datasets = self.get_datasets()
        confirmed, deaths, recovered = [
            self.extract_timeline(val)
            for val in datasets.values()
        ]

        countries = [*confirmed]

        for country in countries:
            for date in dates:
                report = {
                    'confirmed': confirmed[country][date],
                    'deaths': deaths[country][date],
                    'recovered': recovered[country][date]
                }

                self.add_to_database(region=country, date=date,
                                     confirmed=report['confirmed'],
                                     deaths=report['deaths'],
                                     recovered=report['recovered'])
