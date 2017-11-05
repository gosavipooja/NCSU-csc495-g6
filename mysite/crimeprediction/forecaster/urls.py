from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/results/
    url(r'^(?P<zipcode>[0-9]{5,5})/results/$', views.results, name='results'),
]