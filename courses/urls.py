from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = router.urls