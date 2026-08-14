from rest_framework.routers import SimpleRouter

from .views import OrderItemViewSet

router = SimpleRouter()
router.register("order-item", OrderItemViewSet, basename="order-item")

urlpatterns = router.urls
