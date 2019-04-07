from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput
        }
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        if url.rsplit('.', 1)[1] not in valid_extensions:
            raise forms.ValidationError('the url is not valid')
        return url

    def save(self, commit=True, *args, **kwargs):
        img_inst = super(ImageForm, self).save(commit=False, *args, **kwargs)
        image_url = self.cleaned_data['url']
        img_title = '{}.{}'.format(slugify(img_inst.title), image_url.rsplit('.',1)[1])
        response = request.urlopen(image_url)
        img_inst.image.save(img_title, ContentFile(response.read()), save=False)

        if commit:
            img_inst.save()
        return img_inst
