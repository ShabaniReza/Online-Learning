from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer
from .pagination import DefaultPagination
from .filters import CourseFilter


#!ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ


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
    

#!ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['lesson_type']
    search_fields = ['title', 'updated_at']


    def get_queryset(self):

        user = self.request.user
        course_pk = self.kwargs['course_pk']
        course = Course.objects.get(pk=course_pk)
        Lessons = Lesson.objects.filter(course=course)

        if user.is_staff or user.is_superuser:
            return Lessons
        
        if user.role == user.INSTRUCTOR and \
           hasattr(user, 'instructor_profile') and \
           course.instructor == user.instructor_profile:
            return Lessons

        if Enrollment.objects.filter(student=user, course=course, is_completed=False).exists():
            return Lessons
        
        raise PermissionDenied("You are not authorized to view lessons for this course.")



    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]