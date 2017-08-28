from django.conf.urls import include, url

from . import idc,views

urlpatterns = [
    url(r'idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'list/$', views.ListIdcView.as_view(), name="idc_list"),
    ]))
]
