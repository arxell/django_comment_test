import logging

from django.conf import settings
from django.contrib.auth.models import User
import contracts

from app.comment.models import Comment
from app.comment.defs import AddSchemOut


log = logging.getLogger(__name__)


@contracts.contract
def add_comment(add_schema_in):
    """
        :type add_schema_in: AddSchemIn
        :rtype: AddSchemOut
    """
    # check parent
    if add_schema_in.parent_id:
        parent_comment = Comment.objects.filter(
            id=add_schema_in.parent_id
        ).first()
        if not parent_comment:
            return AddSchemOut({
                'status': AddSchemOut.STATUS_ERROR,
                'error': AddSchemOut.ERROR_PARENT_NOT_FOUND,
            })

        if parent_comment:
            add_schema_in.object_id = None
            add_schema_in.type_id = None

    comment = Comment.objects.create(
        object_id=add_schema_in.object_id,
        parent_id=add_schema_in.parent_id,
        text=add_schema_in.text,
        type_id=add_schema_in.type_id,
        user_id=add_schema_in.user_id,
    )

    return AddSchemOut({
        'status': AddSchemOut.STATUS_OK,
        'comment_id': comment.id,
    })
