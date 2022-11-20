from django.contrib import admin
from sales.models import Seller, Brand, Report, ReportType


class SellerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Seller, SellerAdmin)


class BrandAdmin(admin.ModelAdmin):
    pass
admin.site.register(Brand, BrandAdmin)


class ReportTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ReportType, ReportTypeAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'seller', 'brand', 'turnover', 'margin', 'report_type']
admin.site.register(Report, ReportAdmin)