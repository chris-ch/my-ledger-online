from django.conf.urls import include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from oas import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^currencies/$', views.currency_list),
    url(r'^currencies/(?P<code>[A-Z]+)/$', views.currency_detail),
    url(r'^legal_entities/$', views.LegalEntityList.as_view()),
    url(r'^legal_entities/(?P<code>[A-Z]+)/$', views.LegalEntityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
