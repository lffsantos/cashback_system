from rest_framework.routers import DefaultRouter
from core.views import DealerViewSet

app_name = 'core'
#
router = DefaultRouter()
router.register(r'dealer', DealerViewSet)
urlpatterns = router.urls
