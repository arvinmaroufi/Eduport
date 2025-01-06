from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Category, Comment
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def get_pages_to_show(current_page, total_pages):
    """Utility function to determine which pagination pages to show."""
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def home(request):
    latest_courses = Course.objects.filter(status='published').order_by('-created_at')[:4]
    latest_update = Course.objects.filter(status='published').order_by('-updated_at')[:4]
    recommended_courses = Course.objects.filter(status='published', is_recommended=True).order_by('-created_at')[:8]
    return render(request, 'CourseApp/home.html', {'latest_courses': latest_courses, 'latest_update': latest_update,
                                                   'recommended_courses': recommended_courses})


def course_detail(request, slug):
    courses = get_object_or_404(Course, slug=slug)
    chapters = courses.chapter_set.all()
    latest_courses = Course.objects.filter(status='published').exclude(id=courses.id).order_by('-created_at')[:3]
    recommended_courses = Course.objects.filter(status='published', is_recommended=True).exclude(id=courses.id).order_by('-created_at')[:3]
    courses.views += 1
    courses.save()
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, course=courses, user=request.user, parent_id=parent_id)
    return render(request, 'CourseApp/course_detail.html', {'courses': courses, 'chapters': chapters, 'latest_courses': latest_courses,
                                                            'recommended_courses': recommended_courses})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('CourseApp:course_detail', slug=comment.course.slug)


def course_list(request):
    courses = Course.objects.filter(status='published')
    page_number = request.GET.get('page')
    paginator = Paginator(courses, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'CourseApp/course_list.html', {'courses': object_list, 'pages_to_show': pages_to_show})


def category_course(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(status='published', category=category)
    page_number = request.GET.get('page')
    paginator = Paginator(courses, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'CourseApp/category_course.html', {'category': category, 'courses': object_list,
                                                             'pages_to_show': pages_to_show})


def search(request):
    search_course = request.GET.get('search')
    courses = Course.objects.filter(title__icontains=search_course)
    page_number = request.GET.get('page')
    paginator = Paginator(courses, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)
    return render(request, 'CourseApp/course_list.html', {'courses': object_list, 'pages_to_show': pages_to_show})

