from rest_framework import serializers
from django.db.models import Prefetch
from reports.models import Region, Report


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializes an individual country.
    """
    
    class Meta:
        model = Region
        fields = (
            'id',
            'name',
            'iso',
            'latitude',
            'longitude',
            'population',
            'flag_url',
        )


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializes an individual report.
    """
    
    class Meta:
        model = Report
        fields = ('date', 'confirmed', 'deaths', 'recovered')


class CountryTimelineSerializer(serializers.ModelSerializer):
    """
    Serializes a country with all its reports in
    chronological order.
    """

    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = (
            'id',
            'name',
            'iso',
            'flag_url',
            'latitude',
            'longitude',
            'population',
            'reports',
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """
        Perform necessary eager loading of data.
        """
        queryset = queryset.prefetch_related(
            Prefetch('reports', queryset=Report.objects.order_by('date'))
        )
        return queryset


class CountryLatestSerializer(serializers.ModelSerializer):
    """
    Serializes a country with its most recent report.
    """

    latest = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('id', 'name', 'iso', 'flag_url', 'latitude', 'longitude', 'latest')

    def get_latest(self, instance):
        report = Report.objects.filter(region=instance).latest('date')
        return {
            'confirmed': report.confirmed,
            'deaths': report.deaths,
            'recovered': report.recovered,
        }


class GlobalTimelineSerializer(serializers.Serializer):
    """
    Serializers the timeline of the entire world.
    """

    date = serializers.DateField()
    confirmed = serializers.IntegerField()
    recovered = serializers.IntegerField()
    deaths = serializers.IntegerField()
