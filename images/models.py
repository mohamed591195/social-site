from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/shared/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_like', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    
    def get_absolute_url(self):
        return reverse('images:image_detail_page', kwargs={'id': self.id, 'slug': self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
