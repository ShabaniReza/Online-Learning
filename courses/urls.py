from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

courses_router = routers.NestedDefaultRouter(router, 'courses', lookup='course')
courses_router.register('lessons', views.LessonViewSet, basename='course-lessons')


urlpatterns = router.urls + courses_router.urls