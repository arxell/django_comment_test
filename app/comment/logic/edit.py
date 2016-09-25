import logging

from django.db import transaction
from reversion import revisions as reversion
import contracts

from app.comment.models import Comment
from app.comment.defs import EditSchemOut


log = logging.getLogger(__name__)


@contracts.contract
def edit_comment(edit_schema_in):
    """
        :type edit_schema_in: EditSchemIn
        :rtype: tuple(EditSchemOut, Comment|None)
    """
    comment = Comment.objects.filter(
        id=edit_schema_in.comment_id,
        user_id=edit_schema_in.user_id,
    ).first()
    if not comment:
        return EditSchemOut({
            'status': EditSchemOut.STATUS_ERROR,
            'error': EditSchemOut.ERROR_COMMENT_NOT_FOUND,
        }), None

    with transaction.atomic(), reversion.create_revision():
        comment.text = edit_schema_in.text
        comment.save()

        reversion.set_comment('Comment was edited by user')

    return EditSchemOut({'status': EditSchemOut.STATUS_OK}), comment
