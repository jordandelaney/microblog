from .models import BlogPost, Comment

def sidebar_items(request):
    return {
    'sidebar_posts': BlogPost.objects.filter(private=False).order_by('-date_added')[:5],
    }
