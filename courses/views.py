from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Course
from .serializers import CourseSerializer
from .pagination import DefaultPagination
from .filters import CourseFilter

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('instructor').prefetch_related('categories').all()
    serializer_class = CourseSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'categories__name']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]