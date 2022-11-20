from rest_framework import routers
from sales.api import (
    ReportCreateListViewSet,
    SellerCreateListViewSet,
    BrandCreateListViewSet,
    ReportTypeCreateListViewSet
)


router = routers.DefaultRouter()
router.register('reports', ReportCreateListViewSet)
router.register('sellers', SellerCreateListViewSet)
router.register('brands', BrandCreateListViewSet)
router.register('report-types', ReportTypeCreateListViewSet)
urlpatterns = router.urls