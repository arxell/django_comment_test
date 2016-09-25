import logging

from django.db import transaction
from reversion import revisions as reversion
import contracts

from app.comment.defs import AddSchemOut
from app.comment.models import Comment
from app.utils import query_get_one

log = logging.getLogger(__name__)


@contracts.contract
def add_comment(add_schema_in):
    """
        :type add_schema_in: AddSchemIn
        :rtype: tuple(AddSchemOut, Comment|None)
    """
    # check parent
    if add_schema_in.parent_id:
        parent_comment = query_get_one(Comment.objects.filter(
            id=add_schema_in.parent_id
        ))
        if not parent_comment:
            return AddSchemOut({
                'status': AddSchemOut.STATUS_ERROR,
                'error': AddSchemOut.ERROR_PARENT_NOT_FOUND,
            }), None

        if parent_comment:
            add_schema_in.object_id = None
            add_schema_in.type_id = None

    with transaction.atomic(), reversion.create_revision():
        comment = Comment.objects.create(
            object_id=add_schema_in.object_id,
            parent_id=add_schema_in.parent_id,
            text=add_schema_in.text,
            type_id=add_schema_in.type_id,
            user_id=add_schema_in.user_id,
        )
        reversion.set_comment('Comment was created by user')

    return AddSchemOut({
        'status': AddSchemOut.STATUS_OK,
    }), comment
