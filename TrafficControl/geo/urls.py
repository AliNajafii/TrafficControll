from rest_framework.routers import SimpleRouter
from .views import RoadAPIViewSet,TollStationAPIViewSet
from django.urls import path,include

router = SimpleRouter()
router.register(
    'roads',
    RoadAPIViewSet
       
)
router.register(
    'toll-stations',
    TollStationAPIViewSet
)

urlpatterns = router.urls