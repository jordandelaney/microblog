from django import forms
from .models import BlogPost, Comment
from ckeditor.widgets import CKEditorWidget
from django_bleach.forms import BleachField

class PostForm(forms.ModelForm):
    content = BleachField(widget=CKEditorWidget())
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'private']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ""