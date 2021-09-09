from django.urls import path

from blog.views import *

urlpatterns = [
    path('', blog, name=''),
    path('post/', CreateBlog.as_view(), name='post'),
    path('detail/<slug>', blog_detail, name="blog_detail"),
    path('liked/<pk>/', liked, name='liked'),
    path('unliked/<pk>/', unliked, name='unliked'),
    path('my-blogs/', MyBlogs.as_view(), name='my-blogs'),
    path('update/<pk>', UpdateBlog.as_view(), name='update')
]
