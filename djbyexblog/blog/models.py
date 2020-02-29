from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Adjust, ResizeToFit
from djbyexblog.blog.processors import Watermark

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title







class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    subject = models.ForeignKey(Subject,
                                related_name='posts',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    postavatar = ProcessedImageField(upload_to="postavatars/%Y/%m/%d/",
                                     blank=True,
                                     processors=[
                                         ResizeToFit(1600, 500,
                                                     #upscale=False
                                                     ),
                                         Watermark(),
                                     ],
                                     format='JPEG',
                                     options={'quality': 60})

    objects = models.Manager() # dfault manager
    published = PublishedManager() # custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug,])


class Content(models.Model):
    post = models.ForeignKey(Post,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['post'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('blog/content/{}.html'.format(
            self._meta.model_name), {'item': self})

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    #file = models.FileField(upload_to='images')
    file = ProcessedImageField(upload_to="images",
                                 #blank=True,
                                 processors=[
                                     ResizeToFit(1300,1300, upscale=False),
                                     Watermark(),
                                 ],
                                 format='JPEG',
                                 options={'quality': 60})

    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(300, 200)], source='file',
            format='JPEG', options={'quality': 100})


class Video(ItemBase):
    url = models.URLField()
