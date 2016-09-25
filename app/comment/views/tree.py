import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.logic import tree_comment
from app.comment.defs import TreeSchemIn, TreeSchemOut
from app.utils import timeit

log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/tree/

    Input Schema:
        EditSchemIn
    Output Schema:
        EditSchemOut

    Examples:
        /api/comment/v1/tree/?comment_id=1
        /api/comment/v1/tree/?user_id=1
        /api/comment/v1/tree/?type_id=1&object_id=123
    """
    try:
        tree_schema_in = TreeSchemIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        tree_schema_out = TreeSchemOut({
            'status': TreeSchemOut.STATUS_ERROR,
            'error': TreeSchemOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(tree_schema_out.to_native(), status=400)

    tree_schema_out, tree = tree_comment(tree_schema_in)
    result = tree_schema_out.to_native()
    if tree_schema_out.is_status_ok:
        result['tree'] = tree
        return JsonResponse(result)
    else:
        return JsonResponse(result, status=409)
