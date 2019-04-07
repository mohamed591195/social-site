from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageForm
from django.contrib import messages
from .models import Image
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator , EmptyPage
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, 
                      port=settings.REDIS_PORT, 
                      db=settings.REDIS_DB)








def ImageView(request):
    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            new_img = form.save(commit=False)
            new_img.user = request.user
            new_img.save()
            messages.success(request, 'you have created your image successfully')
            return redirect(new_img.get_absolute_url())
    else:
        form = ImageForm(request.GET)
    
    return render(request, 'images/image/create.html', {'form': form, 'section': 'images'})

def ImageDetailView(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr('image:{}:views'.format(image.id))
    return render(request, 'images/image/detail.html', {'section': 'images',
                                                         'image': image,
                                                         'total_views': total_views})





@ajax_required
@login_required
@require_POST
def LikeImg(request):
    
    image_id = int(request.POST.get('id'))
    
    image = get_object_or_404(Image, id=image_id)
    if image.user_like.filter(id=request.user.id).exists():
        image.user_like.remove(request.user)
        create_action(request.user, 'removed like', image)
    else:
        image.user_like.add(request.user)
    likes = image.user_like.count()
    create_action(request.user, 'liked', image)    
    return JsonResponse({'status': 'done', 'likes': likes})

def ImageList(request):
    images = Image.objects.all()
    paging = Paginator(images, 3)
    page = request.GET.get('page',1)
    try:
        images = paging.page(page)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paging.page(paging.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
    
    return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})


