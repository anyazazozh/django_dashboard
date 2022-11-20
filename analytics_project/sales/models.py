from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ReportType(models.Model):
    slug = models.SlugField(null=True)
    name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name


class Report(models.Model):
    date = models.DateField()
    seller = models.ForeignKey(Seller, models.CASCADE)
    brand = models.ForeignKey(Brand, models.CASCADE)
    turnover = models.FloatField(null=True, blank=True) 
    margin = models.FloatField(null=True, blank=True) 
    report_type = models.ForeignKey(ReportType, models.CASCADE, null=True)

    def __str__(self):
        return ' '.join([str(self.date), str(self.seller), str(self.brand)])

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        unique_together = ['date','seller','brand','report_type']