from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^(?P<userid>\d+)/$', views.user_profile, name='user_profile'),
    url(r'^(?P<userid>\d+)/questions$', views.user_questions, name='user_questions'),
    url(r'^(?P<userid>\d+)/answers$', views.user_answers, name='user_answers'),
    url(r'^$', views.user_list, name='user_list')
]
