from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ...models import Tenant
from ..serializers.tenants import TenantSerializer
from ...models import Tenant,Domain
from rest_framework.decorators import api_view

@api_view(['GET'])
def gettenantList(request):
    queryset = Tenant.objects.all()
    serializer = TenantSerializer(queryset, many=True)  # Serialize the queryset with your serializer

    return Response(serializer.data) 


# retrieves a list of all tenants
class TenantListCreateAPIView(ListCreateAPIView):
    permission_classes = [AllowAny,]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def perform_update(self, serializer):
        """
        perform_update is used to update domain model
        """
        Tenant = serializer.save()
        domain = Domain.objects.get(tenant_id=Tenant.id)
        domain.domain = f'{Tenant.schema_name}.localhost'
        domain.save()