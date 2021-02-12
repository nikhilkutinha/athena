from django.urls import path
from . views import (CountryListView, CountryReportView,
                     GlobalTimelineView, GlobalLatestView)

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryReportView.as_view(), name='country-details'),
    path('global/', GlobalTimelineView.as_view(), name='global-latest'),
    path('all/', GlobalLatestView.as_view(), name='global-timeline')
]
