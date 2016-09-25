import logging

from mptt.templatetags.mptt_tags import cache_tree_children
import contracts

from app.comment.defs import TreeSchemOut
from app.comment.models import Comment

log = logging.getLogger(__name__)


@contracts.contract
def _recursive_comment(comment):
    """
        :type comment: Comment
        :rtype: dict
    """
    result = comment.to_dict()
    children = [_recursive_comment(c) for c in comment.get_children()]
    if children:
        result['children'] = children
    return result


@contracts.contract
def build_tree_for_query(query):
    """
        :type query: QuerySet
        :rtype: list
    """
    root_nodes = cache_tree_children(query)
    dicts = []
    for n in root_nodes:
        dicts.append(_recursive_comment(n))
    return dicts


@contracts.contract
def tree_comment(edit_schema_in):
    """
        :type edit_schema_in: TreeSchemIn
        :rtype: tuple(TreeSchemOut, None) | tuple(TreeSchemOut, list)
    """
    if edit_schema_in.comment_id:
        # comments by comment_id
        query = Comment.objects.filter(id=edit_schema_in.comment_id)
    elif (
        edit_schema_in.type_id and
        edit_schema_in.object_id
    ):
        # comments by type_id/object_id
        query = Comment.objects.filter(
            type_id=edit_schema_in.type_id,
            object_id=edit_schema_in.object_id,
        )
    else:
        query = Comment.objects.none()

    if not query.exists():
        return (TreeSchemOut({
            'status': TreeSchemOut.STATUS_ERROR,
            'error': TreeSchemOut.ERROR_COMMENT_NOT_FOUND,
        }), None)

    query = query.get_descendants(include_self=True)
    tree = build_tree_for_query(query)
    return TreeSchemOut({'status': TreeSchemOut.STATUS_OK}), tree
