from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views
import pyaqadvisor.hello

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    #url(r'^api', pyaqadvisor.hello.api, name="api"),
    url(r'^aqadvisor', hello.views.aqadvisor, name="aqadvisor"),
    url(r'^json', hello.views.json, name="json"),
    path('admin/', admin.site.urls),
]
