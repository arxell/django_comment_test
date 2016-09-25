import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.logic import delete_comment
from app.comment.defs import DeleteSchemIn, DeleteSchemOut
from app.utils import timeit

log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/delete/

    Input Schema:
        DeleteSchemIn
    Output Schema:
        DeleteSchemOut

    Examples:
        /api/comment/v1/delete/?comment_id=4&user_id=1
    """
    try:
        delete_schema_in = DeleteSchemIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        delete_schema_out = DeleteSchemOut({
            'status': DeleteSchemOut.STATUS_ERROR,
            'error': DeleteSchemOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(delete_schema_out.to_native(), status=400)

    delete_schema_out = delete_comment(delete_schema_in)

    if delete_schema_out.is_status_ok:
        return JsonResponse(delete_schema_out.to_native())
    else:
        return JsonResponse(delete_schema_out.to_native(), status=409)
