from django.urls import path, include

from . import views

app_name = 'blog'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # All posts page
    path('posts/', views.BlogPostListView.as_view(), name='posts'),

    # All bloggers page
    path('bloggers/', views.UserListView.as_view(), name='bloggers'),

    # Post detail page
    path('post/<int:pk>/<slug:title>/', views.post_detail, name='post-detail'),

    # Blogger detail page
    path('blogger/<str:username>/', views.blogger_detail, name='blogger-detail'),

    # New post
    path('post/new', views.new_post, name='new-post'),

    # New Comment
    path('comment/new/<int:pk>/', views.new_comment, name='new-comment'),

    # Blog post edit
    path('post/<int:pk>/edit', views.edit_post, name='edit-post'),

    # Blog post delete
    path('post/<int:pk>/delete', views.BlogPostDelete.as_view(), name='delete-post'),
]
