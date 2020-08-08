from rest_framework.routers import DefaultRouter

from core.views import PurchaseViewSet, DealerRegisterViewSet

app_name = 'core'

router = DefaultRouter()
router.register(r'dealer', DealerRegisterViewSet)
router.register(r'purcharse', PurchaseViewSet)
urlpatterns = router.urls
