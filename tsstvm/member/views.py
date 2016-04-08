from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from tsstvm.member.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from tsstvm.feeds.models import Feed
from tsstvm.feeds.views import FEEDS_NUM_PAGES

from django.conf import settings as django_settings
from PIL import Image
import os

from .forms import ProfileForm, ChangePasswordForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'member/signup.html', {'form': form})
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)
                profile.save()
            user.save()
            welcome_post = u'{0} has joined the network.'.format(user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()

            return redirect('/')
    else:
        return render(request, 'member/signup.html', {'form': SignUpForm()})

@login_required
def profile(request, username):
    user = request.user
    page_user = get_object_or_404(User, username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id

    print user, page_user
    return render(request, 'member/profile.html', {
        'page_user': page_user,
        'user': user,
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1
        })

@login_required
def network(request):
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'member/network.html', {'users': users})

@login_required
def settings(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.contact_number = form.cleaned_data.get('contact_number')
            user.profile.fb_url = form.cleaned_data.get('facebook_url')
            user.profile.intro = form.cleaned_data.get('self_introduction')
            user.save()
            profile.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile is successfully updated.')
    else:
        form = ProfileForm(instance=user, initial = {
            'job_title':user.profile.job_title,
            'url':user.profile.url,
            'address':user.profile.address,
            'contact_number':user.profile.contact_number,
            'facebook_url':user.profile.fb_url,
            'self_introduction':user.profile.intro,
            })
    return render(request, 'member/settings.html', {'form':form})

@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True
    except Exception, e:
        pass
    return render(request, 'member/picture.html', {'uploaded_picture': uploaded_picture})

@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'

        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)    
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
        return redirect('/settings/picture/?upload_picture=uploaded')
    except Exception, e:
        return redirect('/settings/picture/')

@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w+x, h+y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
    except Exception, e:
        pass
    return redirect('/settings/picture/')


@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password is successfully changed.')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'member/password.html', {'form':form})
