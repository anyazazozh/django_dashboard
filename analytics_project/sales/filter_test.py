from models import Report
from serializers import ReportSerializer
from rest_framework import generics

class ReportList(generics.ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Report.objects.all()
        seller = self.request.query_params.get('seller')
        if seller is not None:
            queryset = queryset.filter(purchaser__username=seller)
        return queryset