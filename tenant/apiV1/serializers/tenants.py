from rest_framework.serializers import ModelSerializer

from ...models import Tenant,Domain


class TenantSerializer(ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

    def create(self, validated_data):
        tenant = Tenant(**validated_data)
        tenant.save()
        domain = Domain(
            domain=f"{validated_data['schema_name']}.localhost",
            tenant_id=tenant.id,
        )
        domain.save()


        return tenant