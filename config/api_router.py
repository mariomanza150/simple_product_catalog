from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from simple_product_catalog.users.api.views import ProductViewSet, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet)


app_name = "api"
urlpatterns = router.urls
