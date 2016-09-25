import logging

import contracts

from app.comment.models import Comment
from app.comment.defs import DeleteSchemOut
from app.utils import query_get_one

log = logging.getLogger(__name__)


@contracts.contract
def delete_comment(delete_schema_in):
    """
        :type delete_schema_in: DeleteSchemIn
        :rtype: DeleteSchemOut
    """
    comment = query_get_one(Comment.objects.filter(
        id=delete_schema_in.comment_id,
        user_id=delete_schema_in.user_id,
    ))
    if not comment:
        return DeleteSchemOut({
            'status': DeleteSchemOut.STATUS_ERROR,
            'error': DeleteSchemOut.ERROR_COMMENT_NOT_FOUND,
        })

    # childrens check
    childrens = comment.get_children()
    if childrens:
        return DeleteSchemOut({
            'status': DeleteSchemOut.STATUS_ERROR,
            'error': DeleteSchemOut.ERROR_COMMENT_HAS_CHILDREN,
        })

    comment.delete()

    return DeleteSchemOut({
        'status': DeleteSchemOut.STATUS_OK,
    })
