from django.urls import path, re_path
from . import views

app_name = 'CourseApp'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'course/(?P<slug>[-\w]+)/', views.course_detail, name='course_detail'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('courses/', views.course_list, name='course_list'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.category_course, name='category_course'),
    path('search/', views.search, name='search_course'),
]
