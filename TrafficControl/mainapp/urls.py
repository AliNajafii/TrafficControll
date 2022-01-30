from rest_framework.routers import SimpleRouter
from .views import OwnerAPIViewSet,CarAPIViewSet
from django.urls import path,include

router = SimpleRouter()
router.register(
    r'owners',
    OwnerAPIViewSet
    
)
router.register(
    r'cars',
    CarAPIViewSet
)


urlpatterns = router.urls