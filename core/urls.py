from rest_framework.routers import DefaultRouter
from django.urls import path
from core.views import PurchaseViewSet, DealerRegisterViewSet, AcumulatedCashbackDealerViewSet

app_name = 'core'

router = DefaultRouter()
router.register(r'dealer', DealerRegisterViewSet)
router.register(r'purchase', PurchaseViewSet)


urlpatterns = router.urls
urlpatterns += [
    path('acumulated-cashback/', AcumulatedCashbackDealerViewSet.as_view(), name='acumulated-cashback'),
]
