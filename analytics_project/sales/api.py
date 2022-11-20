from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report, Seller, Brand, ReportType
from .serializers import (
    ReportSerializer,
    SellerSerializer,
    BrandSerializer,
    ReportTypeSerializer
)


class ReportCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer 


class SellerCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer 


class BrandCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer 


class ReportTypeCreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = ReportType.objects.all()
    serializer_class = ReportTypeSerializer 