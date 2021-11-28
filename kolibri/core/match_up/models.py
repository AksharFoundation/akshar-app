from django.db import models
from morango.models import UUIDField
from kolibri.core.auth.constants import role_kinds
from kolibri.core.auth.permissions.base import RoleBasedPermissions


class MatchUpDetails(models.Model):
    # Morango syncing settings
    morango_model_name = "MatchUpDetails"
    permissions = (
        RoleBasedPermissions(
            target_field="collection",  
            can_be_created_by=(role_kinds.ADMIN),
            can_be_read_by=(role_kinds.ADMIN, role_kinds.COACH, role_kinds.ASSIGNABLE_COACH),
            can_be_updated_by=(role_kinds.ADMIN, role_kinds.COACH),
            can_be_deleted_by=(role_kinds.ADMIN, role_kinds.COACH),
        )
    )
    id = (
        models.AutoField(
            auto_created=True, primary_key=True, serialize=True, verbose_name="ID"
        ),
    )  
    
    #the facility User ID of the mentee
    mentee_id = UUIDField(null=False, unique=False)
    #the name of the mentee
    mentee_name = models.CharField(max_length=200)
    #the facility User ID of the mentor
    mentor_id = UUIDField(null=False, unique=False)
    #the name of the mentor
    mentor_name = models.CharField(max_length=200)
    #the subject for which mathc up is created
    subject = models.CharField(max_length=100)
    #the facility User ID of the supervisor
    supervisor_id = UUIDField(null=False, unique=False)
    #the name of the supervisor name
    supervisor_name = models.CharField(max_length=200)
    #the ID of the facility
    facility_id = UUIDField(null=False, unique=False)