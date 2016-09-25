import logging

import contracts

from app.comment.models import Comment
from app.comment.defs import UserHistorySchemaOut


log = logging.getLogger(__name__)


@contracts.contract
def user_history(user_history_schema_in):
    """
        :type user_history_schema_in: UserHistorySchemaIn
        :rtype: tuple(UserHistorySchemaOut, list(Comment))
    """
    query = Comment.objects.filter(
        user_id=user_history_schema_in.user_id
    )
    if user_history_schema_in.created_at_from:
        query = query.filter(
            created_at__gte=user_history_schema_in.created_at_from
        )
    if user_history_schema_in.created_at_to:
        query = query.filter(
            created_at__lte=user_history_schema_in.created_at_to
        )
    query = query.order_by('created_at')
    history = list(query)
    return UserHistorySchemaOut({'status': UserHistorySchemaOut.STATUS_OK}), history
