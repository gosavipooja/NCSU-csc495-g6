from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^forecaster/predict$', views.predict, name='predict'),
    url(r'^forecaster/trends$', views.trends, name='trends'),
    # ex: /polls/5/results/
    url(r'^(?P<zipcode>[0-9]{5,5})/results/$', views.results, name='results'),
]

