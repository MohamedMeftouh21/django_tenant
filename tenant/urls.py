from django.urls import include,path

urlpatterns = [
    path('',include('tenant.apiV1.urls.tenants')),
]