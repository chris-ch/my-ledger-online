from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from oas import views

urlpatterns = [
    url(r'^currencies/$', views.currency_list),
    url(r'^currencies/(?P<code>[A-Z]+)/$', views.currency_detail),
    url(r'^legal_entities/$', views.legal_entity_list),
    url(r'^legal_entities/(?P<code>[A-Z]+)/$', views.legal_entity_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)