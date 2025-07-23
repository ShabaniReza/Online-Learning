from django_filters.rest_framework import FilterSet
from .models import Course, InstructorProfile

class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'categories__id': ['exact'],
            'price': ['gt', 'lt']
        }

class InstructorFilter(FilterSet):
    class Meta:
        model = InstructorProfile
        fields = {
            'expertise': ['exact'],
            'experience_year': ['gt', 'lt'],
            'rating': ['gt', 'lt']
        }