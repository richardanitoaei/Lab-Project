from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.question_new, name='question_new'),
    url(r'^(?P<questionid>\d+)/$', views.question, name='question'),
    url(r'^(?P<questionid>\d+)/edit$', views.question_edit, name='question_edit'),
    url(r'^(?P<questionid>\d+)/delete$', views.question_delete, name='question_delete'),
    url(r'^(?P<questionid>\d+)/(?P<answerid>\d+)/best$', views.answer_best, name='answer_best'),
    url(r'^(?P<questionid>\d+)/(?P<answerid>\d+)/delete$', views.answer_delete, name='answer_delete'),
    url(r'^$', views.question_list, name='question_list')
]
