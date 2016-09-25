import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.logic import edit_comment
from app.comment.defs import EditSchemIn, EditSchemOut
from app.utils import timeit

log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/edit/

    Input Schema:
        EditSchemIn
    Output Schema:
        EditSchemOut

    Examples:
        /api/comment/v1/edit/?comment_id=1&text=qwe&user_id=123
    """
    try:
        edit_schema_in = EditSchemIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        comment_edit_schema_out = EditSchemOut({
            'status': EditSchemOut.STATUS_ERROR,
            'error': EditSchemOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(comment_edit_schema_out.to_native(), status=400)

    comment_edit_schema_out = edit_comment(edit_schema_in)
    if comment_edit_schema_out.is_status_ok:
        return JsonResponse(comment_edit_schema_out.to_native())
    else:
        return JsonResponse(comment_edit_schema_out.to_native(), status=409)
