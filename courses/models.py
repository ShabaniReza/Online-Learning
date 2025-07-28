from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_file_size


#!ــــــــــــــــــــــــــــــــInstructorــــــــــــــــــــــــــــــــ


class InstructorProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=255)
    experience_year = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='instructor_profile',
    )
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(10.00)],
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


#!ــــــــــــــــــــــــــــــــCategoryــــــــــــــــــــــــــــــــ


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student',
    )


#!ــــــــــــــــــــــــــــــــCategoryــــــــــــــــــــــــــــــــ


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

#!ــــــــــــــــــــــــــــــــCourseــــــــــــــــــــــــــــــــ


class Course(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    ARCHIVED = 'A'
    COURSE_STATUS_CHOICES = {
        DRAFT: 'Draft',
        PUBLISHED: 'Published',
        ARCHIVED: 'Archived',
    }

    title = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Course Description")
    categories = models.ManyToManyField(Category, related_name='course_category')
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.PROTECT,
        related_name='courses',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    status = models.CharField(
        max_length=1,
        choices=COURSE_STATUS_CHOICES,
        default=DRAFT,
    )
    cover_image = models.ImageField(
        upload_to='courses/',
        validators=[validate_file_size],
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


#!ــــــــــــــــــــــــــــــــLessonــــــــــــــــــــــــــــــــ


class Lesson(models.Model):
    VIDEO = 'V'
    TEXT = 'T'
    QUIZ = 'Q'
    LIVE_SESSION = 'L'
    ASSIGNMENT = 'A'
    LESSON_TYPE_CHOICES = {
        VIDEO: 'Video',
        TEXT: 'Text',
        QUIZ: 'Quiz',
        LIVE_SESSION: 'Live_Session',
        ASSIGNMENT: 'Assignment',
    }

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_previewable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    lesson_type = models.CharField(
        max_length=1,
        choices=LESSON_TYPE_CHOICES,
        default=VIDEO,
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


#!ــــــــــــــــــــــــــــــــEnrollmentــــــــــــــــــــــــــــــــ


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


#!ــــــــــــــــــــــــــــــــOrderــــــــــــــــــــــــــــــــ


class Order(models.Model):
    PENDING = 'PE'
    COMPLETED = 'CO'
    CANCELLED = 'CA'
    FAILED = 'FA'
    ORDER_STATUS_CHOICES = {
        PENDING: 'Pending',
        COMPLETED: 'Completed',
        CANCELLED: 'Cancelled',
        FAILED: 'Failed',
    }

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    status = models.CharField(
        max_length=2,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


#!ــــــــــــــــــــــــــــــــOrderItemــــــــــــــــــــــــــــــــ


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='order_items')
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['order', 'course']

    def __str__(self):
        return f"{self.course.title} in Order {self.order.id}"