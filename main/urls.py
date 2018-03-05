from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^questions/', include('questions.urls')),
    url(r'^users/', include('users.urls'))
]
