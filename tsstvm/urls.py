from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tsstvm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    #url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'member/login.html'}, name='login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'member/login.html'}, name='login'),
    
    
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', 'tsstvm.member.views.signup', name='signup'),
    url(r'^settings/$', 'tsstvm.member.views.settings', name='settings'),
    url(r'^settings/password/$', 'tsstvm.member.views.password', name='password'),
    url(r'^settings/picture/$', 'tsstvm.member.views.picture', name='picture'),
    url(r'^settings/upload_picture/$', 'tsstvm.member.views.upload_picture', name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', 'tsstvm.member.views.save_uploaded_picture', name='save_uploaded_picture'),
    
    url(r'^profile/(?P<username>[^/]+)/$', 'tsstvm.member.views.profile', name='profile'),
    url(r'^network/$', 'tsstvm.member.views.network', name='members'),

    url(r'^notifications/$', 'tsstvm.activities.views.notifications', name='notifications'),
    url(r'^notifications/last/$', 'tsstvm.activities.views.last_notifications', name='last_notifications'),
    url(r'^notifications/check/$', 'tsstvm.activities.views.check_notifications', name='check_notifications'),
    
    url(r'^feeds/', include('tsstvm.feeds.urls')),
    url(r'^questions/', include('tsstvm.questions.urls')),
    
    url(r'^articles/', include('tsstvm.articles.urls')),


    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)