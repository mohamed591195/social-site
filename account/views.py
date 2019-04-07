from django.shortcuts import render , get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action

# def LoginView(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             username= cd['username']
#             password = cd['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#             else:

@login_required(login_url='login/')                       
def dash(request):
    targeted_users = [request.user] + list(request.user.following.all())
    actions = Action.objects.filter(user__in=targeted_users)[:10].select_related('user', 'user__profile').prefetch_related('target')
    return render(request, 'account/dash.html', {'section': 'dashboard', 'actions': actions, 'actions': actions})      

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            messages.success(request, 'you have created new account successfully')
            create_action(user, 'created an account and joined us!')
            form = RegisterForm()
    
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def EditView(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        pro_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and pro_form.is_valid():
            user_form.save()
            pro_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    
    else:
        user_form = UserEditForm(instance=request.user)
        pro_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/profile.html', {'user_form': user_form, 'pro_form': pro_form})



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    paging = Paginator(users, 5)
    page = request.GET.get('page', 1)
    try:
        users = paging.page(page)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        users = paging.page(paging.num_pages)
    if request.is_ajax():
        return render(request, 'account/list_ajax.html', {'section': 'people', 'users': users})
    return render(request,
                  'account/list.html',
                  {'section': 'people',
                   'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/detail.html',
                  {'section': 'people',
                   'user': user})
@login_required
@require_POST
@ajax_required
def follow_user(request):
    user_id = request.POST.get('id')
    user = get_object_or_404(User , id=user_id)
    if request.user not in user.followers.all():
        Contact.objects.get_or_create(user_from=request.user, user_to=user)
        create_action(request.user, 'followed', user)
    else:
        Contact.objects.filter(user_from=request.user, user_to=user).delete()
        create_action(request.user, 'unfollowed', user)
    user_followers = user.followers.count()
    return JsonResponse({'status': 'ok', 'followers': user_followers})
    

