from django.urls import path

from ..views.tenants import  TenantListCreateAPIView
from tenant.apiV1.views.tenants import gettenantList

app_name='tenants'

urlpatterns = [
    path('tenants/', TenantListCreateAPIView.as_view(),name='tenants'),

    path('tenant-list/', gettenantList, name='tenant-list'),

    
]