from django import forms
from .models import MyComment, Text, Image

'''
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
'''


from django.forms import ModelForm, inlineformset_factory, Form, BoundField
from django.forms.utils import ErrorList
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.conf import settings

class CustErrorList(ErrorList):
    # custom error list format to use defcss
    def __str__(self):
        return self.as_div()
    def as_div(self):
        if not self:
            return ''
        return format_html('<div class="{}">{}</div>',
                           settings.DEFAULT_CSS['errorlist'],
                           ' '.join( [ force_text(e) for e in self ] )
                           )

class CustBoundField(BoundField):
    # overload label_tag to include default css classes for labels
    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        newcssclass = settings.DEFAULT_CSS['label']
        if attrs is None:
            attrs = {}
        elif 'class' in attrs:
            newcssclass = ' '.join( [ attrs['class'], newcssclass ] ) # NB: order has no impact here (but it does in the style sheet)
        attrs.update( { 'class': newcssclass } )
        # return the output of the original method with the modified attrs
        return super( CustBoundField, self ).label_tag( contents, attrs, label_suffix )

def custinit(self, subclass, *args, **kwargs):
    # overload Form or ModelForm inits, to use default CSS classes for widgets
    super( subclass, self ).__init__(*args, **kwargs)
    self.error_class = CustErrorList # change the default error class

    # Loop on fields and add css classes
    # Warning: must loop on fields, not on boundfields, otherwise inline_formsets break
    for field in self.fields.values():
        thiswidget = field.widget
        if thiswidget .is_hidden:
            continue
        newcssclass = settings.DEFAULT_CSS[ thiswidget.__class__.__name__ ]
        thisattrs = thiswidget.attrs
        if 'class' in thisattrs:
            newcssclass = ' '.join( [ thisattrs['class'], newcssclass ] ) # NB: order has no impact here (but it does in the style sheet)
        thisattrs.update( { 'class': newcssclass } )

def custgetitem(self, name):
    # Overload of Form getitem to use the custom BoundField with
    # css-classed labels. Everything here is just a copy of django's version,
    # apart from the call to CustBoundField
    try:
        field = self.fields[name]
    except KeyError:
        raise KeyError(
            "Key '%s' not found in '%s'. Choices are: %s." % (
                name,
                self.__class__.__name__,
                ', '.join(sorted(f for f in self.fields)),
            )
        )
    if name not in self._bound_fields_cache:
        self._bound_fields_cache[name] = CustBoundField( self, field, name )
        # In the original version, field.get_bound_field is called, but
        # this method only calls BoundField. It is much easier to
        # subclass BoundField and call it directly here
    return self._bound_fields_cache[name]

class DefaultCssModelForm(ModelForm):
    # Defines the new reference ModelForm, with default css classes
    error_css_class = settings.DEFAULT_CSS['error']
    required_css_class = settings.DEFAULT_CSS['required']
    label_css_class = settings.DEFAULT_CSS['label']



    def __init__(self, *args, **kwargs):
        custinit(self, DefaultCssModelForm, *args, **kwargs)

    def __getitem__(self, name):
        return custgetitem(self, name)

class DefaultCssForm(Form):
    # Defines the new reference Form, with default css classes

    error_css_class = settings.DEFAULT_CSS['error']
    required_css_class = settings.DEFAULT_CSS['required']

    def __init__(self, *args, **kwargs):
        custinit(self, DefaultCssForm, *args, **kwargs)

    def __getitem__(self, name):
        return custgetitem(self, name)





class MyCommentForm(DefaultCssModelForm):
    class Meta:
        model = MyComment
        fields = ('body',)


class SearchForm(DefaultCssForm):
    query = forms.CharField()



class ContentAddTextForm(DefaultCssModelForm):
    class Meta:
        model = Text
        fields = ('title', 'content',)

class ContentAddImageForm(DefaultCssModelForm):
    class Meta:
        model = Image
        fields = ('title', 'file',)



