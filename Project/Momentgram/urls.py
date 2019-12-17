from django.conf.urls import url

from django.contrib import admin
from . import views
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static # new
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    url(r'^$', views.index, name='init'),
    url(r'^login/$', views.signIn, name='login'),
    url(r'^signup/$', views.register, name='signup'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^post/$', views.publish_post, name='publish'),
    url(r'^view_post/(?P<id>.*)/$', views.view_post, name='view_post'),
    url(r'^manage_friend/(?P<username>.*)/(?P<index>.*)/$', views.manage_friend, name='manage_complete'),
    url(r'^manage_friend/(?P<username>.*)/$', views.manage_friend, name='manage'),
    url(r'^search_users=(?P<isProfile>.*)/searched=(?P<searched>.*)/(?P<index>.*)/$', views.search_users, name='search_users_complete'),
    url(r'^search_users=(?P<isProfile>.*)/$', views.search_users, name='search_users'),
    url(r'^profile=(?P<username>.*)/(?P<index>.*)/$', views.show_profile, name='show_profile_complete'),
    url(r'^profile=(?P<username>.*)/$', views.show_profile, name='show_profile'),
    url(r'^timeline/index=(?P<index>.*)/$', views.timeline, name='full_timeline'),
    url(r'^timeline/$', views.timeline, name='timeline'),
    url(r'^chat/(?P<username>.*)$', views.chat, name='chat')


    #path('admin/', admin.site.urls),
    #path('', include('posts.urls'))

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

