from django.forms import ModelForm, inlineformset_factory, Form, BoundField
from django.forms.utils import ErrorList
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.conf import settings

from django import forms
from .models import MyComment, Text, Image


class MyCommentForm(ModelForm):
    class Meta:
        model = MyComment
        fields = ('body',)


class SearchForm(Form):
    query = forms.CharField()



class ContentAddTextForm(ModelForm):
    class Meta:
        model = Text
        fields = ('title', 'content',)

class ContentAddImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'file',)
