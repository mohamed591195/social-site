from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.ImageView, name='create_image_page'),
    path('image/<int:id>/<slug:slug>/', views.ImageDetailView, name='image_detail_page'),
    path('like/',views.LikeImg, name='image_like'),
    path('', views.ImageList, name='imagelist_page')
]