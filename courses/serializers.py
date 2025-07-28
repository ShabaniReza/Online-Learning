from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Course, Lesson, InstructorProfile, Student, Category


#!ــــــــــــــــــــــــــــــــCategoryــــــــــــــــــــــــــــــــ


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


#!ــــــــــــــــــــــــــــــــCourseــــــــــــــــــــــــــــــــ


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'categories', 'created_at', 'instructor', 'price', 'cover_image']


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


# @ ___________________For serializer_class of InstructorViewSet___________________

class InstructorLessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title']

class InstructorCourseSerializer(ModelSerializer):
    lessons = InstructorLessonSerializer()
    class Meta:
        model = Course
        fields = ['title', 'description', 'categories', 'lessons']

class InstructorSerializer(ModelSerializer):
    user = StringRelatedField()
    courses = InstructorCourseSerializer()

    class Meta:
        model = InstructorProfile
        fields = ['first_name', 'last_name', 'user', 'expertise', 'experience_year', 'rating', 'courses']

class SimpleInstructorSerializer(ModelSerializer):    
    class Meta:
        model = InstructorProfile
        fields = ['user', 'first_name', 'last_name', 'expertise', 'experience_year', 'rating']

# @ ___________________For GET method in 'me' action of InstructorViewSet___________________

class IpLessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'content', 'order', 'created_at', 'updated_at', 'lesson_type', 'video_url']

class IpCourseSerializer(ModelSerializer):
    lessons = IpLessonSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ['title', 'description', 'categories', 'created_at', 'price', 'status', 'cover_image', 'lessons']

class InstructorProfileSerializer(ModelSerializer):
    user = StringRelatedField(read_only=True)
    courses = IpCourseSerializer(read_only=True)

    class Meta:
        model = InstructorProfile
        fields = ['first_name', 'last_name', 'user', 'expertise', 'experience_year', 'rating', 'courses']

# @ ___________________For PUT method in 'me' action of InstructorViewSet___________________

class UpdateInstructorProfileSerializer(ModelSerializer):
    user = StringRelatedField()

    class Meta:
        model = InstructorProfile
        fields = ['first_name', 'last_name', 'user']


#!ــــــــــــــــــــــــــــــــStudentــــــــــــــــــــــــــــــــ


class StudentSerializer(ModelSerializer):
    user = StringRelatedField()
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'user']