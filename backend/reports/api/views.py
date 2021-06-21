from rest_framework import generics
from reports.models import Region, Report
from django.db.models import Sum


from .serializers import (
    CountryLatestSerializer,
    CountryTimelineSerializer,
    CountrySerializer,
    GlobalTimelineSerializer,
)


class CountryListView(generics.ListAPIView):
    queryset = Region.objects.filter(type=Region.COUNTRY)
    serializer_class = CountrySerializer


class CountryReportView(generics.RetrieveAPIView):
    serializer_class = CountryTimelineSerializer

    def get_queryset(self):
        qs = Region.objects.filter(type=Region.COUNTRY)
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs


class GlobalLatestView(generics.ListAPIView):
    serializer_class = CountryLatestSerializer

    def get_queryset(self):
        countries = Region.objects.filter(
            type=Region.COUNTRY, reports__isnull=False
        ).distinct()
        return countries


class GlobalTimelineView(generics.ListAPIView):
    serializer_class = GlobalTimelineSerializer

    def get_queryset(self):
        timeline = (
            Report.objects.filter()
            .values('date')
            .order_by('date')
            .annotate(
                confirmed=Sum('confirmed'),
                deaths=Sum('deaths'),
                recovered=Sum('recovered'),
            )
        )

        return timeline
