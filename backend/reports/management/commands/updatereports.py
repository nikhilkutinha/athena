import csv
import json
from datetime import datetime, time

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Region, Report

TIMELINE_KEYS = ['confirmed', 'deaths', 'recovered']
BASE_DIR = settings.BASE_DIR

class Command(BaseCommand):

    help = 'Synchronizes latest reports in the database.'

    def add_arguments(self, parser):
        parser.add_argument('files', action='store_false')
        parser.add_argument('confirmed', nargs='?', type=str)
        parser.add_argument('deaths', nargs='?', type=str)
        parser.add_argument('recovered', nargs='?', type=str)

    def handle(self, *args, **options):
        datasets = self.get_datasets()

        confirmed, deaths, recovered = [
            self.normalize_dataset(d) for d in datasets.values()
        ]

        countries = [*confirmed]

        for country in countries:
            for date in dates:
                report = {
                    'confirmed': confirmed[country][date],
                    'deaths': deaths[country][date],
                    'recovered': recovered[country][date],
                }

                self.add_report_to_database(
                    region=country,
                    date=date,
                    confirmed=report['confirmed'],
                    deaths=report['deaths'],
                    recovered=report['recovered'],
                )

    def get_datasets(self, *args, **options):
        """
        Get dataset from filepaths if they were passed in via
        arguments else get them from github.

        Args:
            None

        Returns:
            A dict representation containing various dataset.
        """

        if 'files' in options:
            return self.get_datasets_from_files()

        else:
            self.stdout.write(
                self.style.WARNING(
                    'You did not provide files to parse, '
                    'hence we\'ll be using datasets available'
                    'at https://github.com/cssegisanddata'
                )
            )
            return self.get_datasets_from_github()

    def get_datasets_from_github(self):
        dataset = {}

        with open(BASE_DIR / 'files/urls.json') as f:
            urls = json.load(f)['urls']

        for timeline in TIMELINE_KEYS:
            res = requests.get(urls[timeline])
            content = res.content.decode('utf-8')
            dataset[timeline] = csv.reader(content.splitlines(), delimiter=',')

        return dataset

    def get_datasets_from_file(self, **options):
        dataset = {}

        for timeline in TIMELINE_KEYS:
            with open(options[timeline]) as f:
                csv_file = csv.reader(f)
            dataset[timeline] = csv_file

        return dataset

    def normalize_dataset(self, dataset):
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
        dates = [self.format_date(date) for date in header[4:]]
        timeline = {}

        for line in dataset:
            _, country, _, _, *counts = line

            timeline[country] = timeline.get(country, {})

            for index, date in enumerate(dates):
                timeline[country][date] = timeline[country].get(date, 0)
                timeline[country][date] += int(counts[index])

        return timeline

    def add_report_to_database(self, **kwargs):
        """
        Update or create a report for a specific region or country.

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
            a boolean depecting if the report was created or updated.

            True = created
            False = updated.
        """

        kwargs['region'] = Region.objects.get(
            name=kwargs['region'], type=Region.COUNTRY
        )

        report, created = Report.objects.update_or_create(
            region=kwargs['region'], date=kwargs['date'], defaults=kwargs
        )

        return report, created

    def format_date(self, date):
        return datetime.strptime(date, '%m/%d/%y').date().__str__()
