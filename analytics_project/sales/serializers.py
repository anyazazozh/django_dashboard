from rest_framework import serializers, renderers

from .models import Report, Seller, Brand, ReportType


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id', 
            'date', 
            'seller', 
            'brand', 
            'turnover', 
            'margin', 
            'report_type'
        ]


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            'id', 
            'name'
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id', 
            'name'
        ]

class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = [
            'id', 
            'name',
            'slug'
        ]