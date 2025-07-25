from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .models import Course, Lesson, Enrollment, InstructorProfile, Student
from .serializers import CourseSerializer, LessonSerializer, SimpleLessonSerializer, InstructorSerializer, InstructorProfileSerializer, UpdateInstructorProfileSerializer, StudentSerializer, SimpleInstructorSerializer
from .pagination import DefaultPagination
from .filters import CourseFilter, InstructorFilter
from .permissions import OnlyAdminAndInstructor


#!ــــــــــــــــــــــــــــــــCourseــــــــــــــــــــــــــــــــ


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
    

#!ــــــــــــــــــــــــــــــــLessonــــــــــــــــــــــــــــــــ


class LessonViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['lesson_type']
    search_fields = ['title', 'updated_at']
    pagination_class = DefaultPagination


    def get_queryset(self):

        user = self.request.user
        course_pk = self.kwargs['course_pk']
        course = Course.objects.get(pk=course_pk)
        Lessons = Lesson.objects.filter(course=course)
        Free_lessons = Lesson.objects.filter(course=course, is_previewable=True)

        # * First two lines check if user is staff/superuser
        # * Third line check if user enrolled in this course
        # * Other lines check if user is instructor of course
        if user.is_staff or \
           user.is_superuser or \
           Enrollment.objects.filter(student=user, course=course, is_completed=False).exists() or \
           user.role == user.INSTRUCTOR and \
           hasattr(user, 'instructor_profile') and \
           course.instructor == user.instructor_profile:
            return Lessons
        
        # * Only shows lessons that is previewable 
        else:
            return Free_lessons


    def get_serializer_class(self):
        user = self.request.user
        course_pk = self.kwargs['course_pk']
        course = Course.objects.get(pk=course_pk)

        if user.is_staff or \
           user.is_superuser or \
           Enrollment.objects.filter(student=user, course=course, is_completed=False).exists() or \
           Lesson.is_previewable==True or \
           user.role == user.INSTRUCTOR and \
           hasattr(user, 'instructor_profile') and \
           course.instructor == user.instructor_profile:
            return LessonSerializer

        else:
            return SimpleLessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    

#!ــــــــــــــــــــــــــــــــInstructorــــــــــــــــــــــــــــــــ


class InstructorViewSet(ModelViewSet):
    queryset = InstructorProfile.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = InstructorFilter
    search_fields = ['first_name', 'last_name', 'expertise']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InstructorSerializer
        return SimpleInstructorSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'], permission_classes=[OnlyAdminAndInstructor])
    def me(self, request):
        instructor = InstructorProfile.objects.get(user__id=self.request.user.id)
        if request.method == 'GET':
            serializer = InstructorProfileSerializer(instructor)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UpdateInstructorProfileSerializer(instructor, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

#!ــــــــــــــــــــــــــــــــStudentــــــــــــــــــــــــــــــــ


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'user__username', 'user__email']

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        student = Student.objects.get(user__id=self.request.user.id)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
        elif request.method == 'POST':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)