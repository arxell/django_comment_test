import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.logic import add_comment
from app.comment.defs import AddSchemIn, AddSchemOut
from app.utils import timeit


log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/add/

    Input Schema:
        AddSchemIn
    Output Schema:
        AddSchemOut

    Examples:
        /api/comment/v1/add/?type_id=1&object_id=123&text=qwe&parent=22&user_id=123
    """
    try:
        add_schema_in = AddSchemIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        add_schema_out = AddSchemOut({
            'status': AddSchemOut.STATUS_ERROR,
            'error': AddSchemOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(add_schema_out.to_native(), status=400)

    add_schema_out = add_comment(add_schema_in)

    if add_schema_out.is_status_ok:
        return JsonResponse(add_schema_out.to_native())
    else:
        return JsonResponse(add_schema_out.to_native(), status=409)
