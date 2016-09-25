from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from mptt.models import MPTTModel, TreeForeignKey
from reversion import revisions as reversion
import contracts


@reversion.register
class Comment(MPTTModel):

    user_id = models.IntegerField()
    text = models.CharField(max_length=1024)

    type_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True
    )

    parent = TreeForeignKey(
        'self',
        blank=True,
        db_index=True,
        null=True,
        related_name='children',
    )

    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = []

    @contracts.contract
    def to_dict(comment):
        """
            :type comment: Comment
            :rtype: dict
        """
        return \
            {
                'id': comment.pk,
                'text': comment.text,
                'user_id': comment.user_id,
                'type_id': comment.type_id,
                'object_id': comment.object_id,
                'modified_at': comment.modified_at.isoformat(),
                'created_at': comment.created_at.isoformat(),
            }

    def __str__(self):
        return '{}'.format(self.id)


@receiver(pre_save, sender=Comment)
def check(instance, **kwargs):
    comment = instance

    if comment.parent_id and (comment.type_id or comment.object_id):
        raise ValueError('set parent_id or type_id/object_id')
