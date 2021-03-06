from __future__ import unicode_literals

from django.db import models

from kolibri.core.auth.constants import role_kinds
from kolibri.core.auth.models import AbstractFacilityDataModel
from kolibri.core.auth.models import Collection
from kolibri.core.auth.models import FacilityUser
from kolibri.core.auth.permissions.base import RoleBasedPermissions
from kolibri.core.fields import DateTimeTzField
from kolibri.core.fields import JSONField
from kolibri.core.notifications.models import LearnerProgressNotification
from kolibri.utils.time_utils import local_now


class Lesson(AbstractFacilityDataModel):
    """
    A Lesson is a collection of non-topic ContentNodes that is linked to
    a Classroom and LearnerGroups within that Classroom.
    """

    permissions = RoleBasedPermissions(
        target_field="collection",
        can_be_created_by=(role_kinds.ADMIN, role_kinds.COACH),
        can_be_read_by=(role_kinds.ADMIN, role_kinds.COACH),
        can_be_updated_by=(role_kinds.ADMIN, role_kinds.COACH),
        can_be_deleted_by=(role_kinds.ADMIN, role_kinds.COACH),
    )

    title = models.CharField(max_length=50)
    description = models.CharField(default="", blank=True, max_length=200)
    """
    Like Exams, we store an array of objects with the following form:
    {
      contentnode_id: string,
      content_id: string,
      channel_id: string
    }
    """
    resources = JSONField(default=[], blank=True)
    # If True, then the Lesson should be viewable by Learners
    is_active = models.BooleanField(default=False)

    # The Classroom-type Collection for which the Lesson is created
    collection = models.ForeignKey(
        Collection, related_name="lessons", blank=False, null=False
    )

    created_by = models.ForeignKey(
        FacilityUser, related_name="lessons_created", blank=False, null=False
    )
    date_created = DateTimeTzField(default=local_now, editable=False)

    def get_all_learners(self):
        """
        Get all Learners that are somehow assigned to this Lesson
        """
        assignments = self.lesson_assignments.all()
        learners = FacilityUser.objects.none()
        for a in assignments:
            learners = learners.union(a.collection.get_members())
        return learners

    def __str__(self):
        return "Lesson {} for Classroom {}".format(self.title, self.collection.name)

    def delete(self, using=None, keep_parents=False):
        """
        We delete all notifications objects whose lesson is this lesson id.
        """
        LearnerProgressNotification.objects.filter(lesson_id=self.id).delete()
        super(Lesson, self).delete(using, keep_parents)

    # Morango fields
    morango_model_name = "lesson"

    def infer_dataset(self, *args, **kwargs):
        return self.cached_related_dataset_lookup("collection")

    def calculate_partition(self):
        return self.dataset_id


class LessonAssignment(AbstractFacilityDataModel):
    """
    Links LearnerGroup- or Classroom-type Collections to a Lesson
    """

    permissions = RoleBasedPermissions(
        target_field="collection",
        can_be_created_by=(),
        can_be_read_by=(role_kinds.ADMIN, role_kinds.COACH),
        can_be_updated_by=(role_kinds.ADMIN, role_kinds.COACH),
        can_be_deleted_by=(),
    )

    lesson = models.ForeignKey(
        Lesson, related_name="lesson_assignments", blank=False, null=False
    )
    collection = models.ForeignKey(
        Collection, related_name="assigned_lessons", blank=False, null=False
    )
    assigned_by = models.ForeignKey(
        FacilityUser, related_name="assigned_lessons", blank=False, null=False
    )

    def __str__(self):
        return "Lesson Assignment {} for Collection {}".format(
            self.lesson.title, self.collection.name
        )

    # Morango fields
    morango_model_name = "lessonassignment"

    def infer_dataset(self, *args, **kwargs):
        return self.cached_related_dataset_lookup("assigned_by")

    def calculate_source_id(self):
        return "{lesson_id}:{collection_id}".format(
            lesson_id=self.lesson_id, collection_id=self.collection_id
        )

    def calculate_partition(self):
        return self.dataset_id


class IndividualSyncableLesson(AbstractFacilityDataModel):
    """
    Represents a Lesson and its assignment to a particular user
    in such a way that it can be synced to a single-user device.
    Note: This is not the canonical representation of a user's
    relation to a lesson (which is captured in a LessonAssignment
    combined with a user's Membership in an associated Collection;
    the purpose of this model is as a derived/denormalized
    representation of a specific user's lesson assignments).
    """

    morango_model_name = "individualsyncablelesson"

    user = models.ForeignKey(FacilityUser)
    collection = models.ForeignKey(Collection)
    lesson_id = models.UUIDField()

    serialized_lesson = JSONField()

    def infer_dataset(self, *args, **kwargs):
        return self.cached_related_dataset_lookup("user")

    def calculate_source_id(self):
        return self.lesson_id

    def calculate_partition(self):
        return "{dataset_id}:user-ro:{user_id}".format(
            dataset_id=self.dataset_id, user_id=self.user_id
        )

    @classmethod
    def serialize_lesson(cls, lesson):
        serialized = lesson.serialize()
        for key in ["is_active", "created_by_id", "date_created", "collection_id"]:
            serialized.pop(key, None)
        return serialized

    @classmethod
    def deserialize_lesson(cls, serialized_lesson):
        lesson = Lesson.deserialize(serialized_lesson)
        lesson.is_active = True
        return lesson
