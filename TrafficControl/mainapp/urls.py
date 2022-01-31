from rest_framework.routers import SimpleRouter
from .views import (
    OwnerAPIViewSet,
    CarAPIViewSet,
    CarTrafficAPIViewSet
    )
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

router.register(
    r'traffics',
    CarTrafficAPIViewSet
)

urlpatterns = router.urls