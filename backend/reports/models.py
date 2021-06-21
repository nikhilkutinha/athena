from django.db import models
from django.core.validators import FileExtensionValidator


class Region(models.Model):
    iso = models.CharField(max_length=2, blank=True, default=None)
    name = models.CharField(max_length=128)
    flag = models.FileField(upload_to='flags', validators=[FileExtensionValidator(['svg', 'png'])])
    longitude = models.DecimalField(decimal_places=8, max_digits=16, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=8, max_digits=16, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    population = models.PositiveIntegerField(blank=True, null=True)

    COUNTRY = 'CTY'
    PROVINCE = 'PRV'
    REGION_TYPES = [
        (COUNTRY, 'Country'), 
        (PROVINCE, 'Province')
    ]

    type = models.CharField(choices=REGION_TYPES, max_length=3)

    @property
    def flag_url(self):
        if self.flag:
            return self.flag.get_url()

        if not self.iso: return
        
        return 'https://raw.githubusercontent.com/lipis/flag-icon-css/master/flags/4x3/%s.svg' % self.iso.lower()
    
    def __str__(self):
        return self.name

class Report(models.Model):
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='reports')
    confirmed = models.PositiveIntegerField(blank=True, null=True)
    active = models.PositiveIntegerField(blank=True, null=True)
    deaths = models.PositiveIntegerField(blank=True, null=True)
    recovered = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.region.name, self.date)
