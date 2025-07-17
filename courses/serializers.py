from rest_framework.serializers import ModelSerializer
from .models import Course







class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'descriptions', 'categories', 'created_at', 'instructor', 'price', 'status', 'cover_image']