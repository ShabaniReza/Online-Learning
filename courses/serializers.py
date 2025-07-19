from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Course, Lesson


#!ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'descriptions', 'categories', 'created_at', 'instructor', 'price', 'cover_image']


#!ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ


class LessonSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'content', 'order', 'is_previewable', 'created_at', 'updated_at', 'course']