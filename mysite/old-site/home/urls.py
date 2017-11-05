from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'home'

urlpatterns = [
    # .com/home/
    url(r'^$', TemplateView.as_view(template_name='home/index.html'), name='homepage'),
    url(r'^test/', TemplateView.as_view(template_name='home/test.html'), name='testpage'),
    url(r'^your_name/', TemplateView.as_view(template_name='home/index.html'), name='your_name'),
]
