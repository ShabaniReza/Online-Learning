from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from .models import Course, Lesson, InstructorProfile


#!ــــــــــــــــــــــــــــــــCourseــــــــــــــــــــــــــــــــ


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'descriptions', 'categories', 'created_at', 'instructor', 'price', 'cover_image']


#!ــــــــــــــــــــــــــــــــLessonــــــــــــــــــــــــــــــــ


class SimpleLessonSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'order', 'is_previewable', 'created_at', 'updated_at', 'course']
    


class LessonSerializer(ModelSerializer):
    course = StringRelatedField()

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'content', 'order', 'is_previewable', 'created_at', 'updated_at', 'course']


#!ــــــــــــــــــــــــــــــــInstructorــــــــــــــــــــــــــــــــ


class InstructorSerializer(ModelSerializer):
    username = SerializerMethodField(read_only=True)

    class Meta:
        model = InstructorProfile
        fields = ['first_name', 'last_name', 'username', 'expertise', 'experience_year', 'rating']

    def get_username(self, obj):
        return obj.user.username



class SimpleInstructorSerializer(ModelSerializer):
    username = SerializerMethodField()

    class Meta:
        model = InstructorProfile
        fields = ['first_name', 'last_name', 'username']

        def get_username(self, obj):
            return obj.user.username