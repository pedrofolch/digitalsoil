from django import forms
from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = [
            "blog",
            'title',
            'slug',
            'headline',
            'user',
            "image",
            'height_field',
            'width_field',
            "content",

            "draft",
            'read_time',
            'authors',
            'rating'
        ]
