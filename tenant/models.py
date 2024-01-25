from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import DomainMixin, TenantMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
import subprocess
from .management.commands.create_tenant_superuser import Command as CreateTenantSuperUserCommand
import os
from django_tenants.models import TenantMixin
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context
from django.contrib.auth.models import Group  # Import Group model

from django.contrib.auth import get_user_model
from base.models import CustomUser

from django_sharding_library.decorators import model_config
from django_sharding_library.fields import TableShardedIDField
from django_sharding_library.models import TableStrategyModel




class Tenant(TenantMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    tenant_name = models.CharField(max_length=50)
    tenant_image = models.ImageField(null=True, blank=True, upload_to="profile")

    featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=False, blank=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and
    # synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

 

    class Meta:
        ordering = ('-featured', '-updated_at')

    def __str__(self):
        return f"{self.tenant_name}"
    def save(self, *args, **kwargs):
        is_new_tenant = not self.pk
        super().save(*args, **kwargs)
        
        if is_new_tenant:
            # Create a superuser for the newly created tenant
            superuser_username = 'admin'
            superuser_email = 'admin@example.com'
            superuser_password = 'securepassword'
            
            with schema_context(self.schema_name):
                try:
                    user = CustomUser.objects.create_superuser(
                        email=superuser_email,
                        password=superuser_password,
                        first_name='Admin',  
                        last_name='User',   
                    )

                    # Add the group list here directly
                    group_names = ['premium', 'free']

                    # Get or create the groups based on their names
                    groups = [Group.objects.get_or_create(name=name)[0] for name in group_names]

                    user.groups.add(*groups)
                except Exception as e:
                    print("Error creating superuser:", e)

class Domain(DomainMixin):
    pass




@receiver(post_save, sender=Tenant)
def create_tenant_superuser(sender, instance, created, **kwargs):
    if created:
        tenant_schema_name = instance.schema_name
        superuser_first_name = instance.user.first_name
        superuser_last_name=instance.user.last_name
        superuser_email = instance.user.email
        superuser_password = instance.user.password
        print("superuser_last_name",instance.user.last_name)

        command = [
            'python', 'manage.py', 'create_tenant_superuser',
            tenant_schema_name, superuser_email,superuser_first_name,superuser_last_name , superuser_password
        ]
        
        subprocess.run(command)




