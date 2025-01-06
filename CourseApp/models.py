from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django_resized import ResizedImageField
from datetime import timedelta
from django.urls import reverse


LEVEL = (
    ("introductory", "سطح مقدماتی"),
    ("advanced", "سطح پیشرفته"),
    ("introductory_advanced", "سطح از مقدماتی تا پیشرفته")
)

IS_PAID = (
    ("free", "رایگان"),
    ("premium", "پولی"),
)

COURSE_STATUS = (
    ("completed", "تکمیل شده"),
    ("in_progress", "درحال برگزاری"),
    ("starting_soon", "شروع به زودی"),
)

STATUS = (
    ("draft", "پیش نویس شود"),
    ("published", "منتشر شود"),
)


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='subs', verbose_name='والد')
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='نامک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('CourseApp:category_course', args=[self.slug])

    def __str__(self):
        return self.title


class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مدرس دوره')
    category = models.ManyToManyField(Category, related_name='courses', verbose_name='دسته بندی')
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان دوره')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='نامک')
    description = RichTextUploadingField(verbose_name='توضیحات دوره')
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان دوره')
    video_count = models.PositiveIntegerField(verbose_name='تعداد ویدیوها')
    price = models.IntegerField(blank=True, null=True, verbose_name='قیمت دوره')
    discount = models.SmallIntegerField(blank=True, null=True, verbose_name='تخفیف')
    is_paid = models.CharField(choices=IS_PAID, max_length=10, default='premium', verbose_name='آیا دوره پولی است یا رایگان؟')
    # thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True, help_text='ارتفاع عکس: 200 پیکسل', verbose_name='تصویر دوره')
    thumbnail = ResizedImageField(size=[600, 500], upload_to='course_thumbnails/', blank=True, null=True, help_text='عرض عکس حداکثر 600 پیکسل و ارتفاع عکس حداکثر 500 پیکسل باشد')
    level = models.CharField(choices=LEVEL, max_length=30, default='introductory', verbose_name='سطح دوره')
    course_status = models.CharField(choices=COURSE_STATUS, max_length=20, default='in_progress', verbose_name='وضعیت دوره')
    status = models.CharField(choices=STATUS, max_length=10, default='draft', verbose_name='وضعیت')
    is_recommended = models.BooleanField(default=False, verbose_name='آیا دوره، پیشنهادی است؟')
    views = models.IntegerField(default=0, editable=False, verbose_name='بازدید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'

    def formatted_duration(self):
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if total_seconds < 3600:
            return f"{minutes}:{seconds:02}"

        return f"{hours}:{minutes}:{seconds:02}"

    def get_absolute_url(self):
        return reverse('CourseApp:course_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Faq(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره مربوطه')
    title = models.CharField(max_length=100, verbose_name='عنوان سوال')
    description = models.TextField(verbose_name='جواب سوال')
    order = models.PositiveIntegerField(verbose_name='ترتیب سوال و جواب ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'

    def __str__(self):
        return self.title


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='دوره مربوطه')
    title = models.CharField(max_length=150, unique=True, verbose_name='عنوان فصل')
    order = models.PositiveIntegerField(verbose_name='ترتیب فصل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'فصل'
        verbose_name_plural = 'فصل ها'

    def __str__(self):
        return f'{self.title} - {self.course.title}'


class Video(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='فصل مربوطه')
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان ویدیو')
    video_link = models.CharField(max_length=500, verbose_name='لینک ویدیو')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True, help_text='ارتفاع عکس: 500 پیکسل', verbose_name='تصویر دوره')
    order = models.PositiveIntegerField(unique=True, verbose_name='ترتیب ویدیو')
    is_paid = models.BooleanField(default=False, verbose_name='آیا برای دیدن نیاز به خرید دوره است؟')
    duration = models.DurationField(default=timedelta(), verbose_name='مدت زمان ویدیو')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیو ها'

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله مربوطه')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='نظر والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    body = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')
    status = models.CharField(choices=STATUS, max_length=10, default='draft', verbose_name='وضعیت')

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

