import logging

from django.http.response import JsonResponse
from reversion.models import Version
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.defs import EditHistorySchemIn, EditHistorySchemOut
from app.comment.models import Comment
from app.utils import timeit

log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/edit/

    Input Schema:
        EditHistorySchemIn
    Output Schema:
        EditHistorySchemOut

    Examples:
        /api/comment/v1/edit/history?comment_id=238925
    """
    try:
        edit_history_schema_in = EditHistorySchemIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        edit_history_schema_out = EditHistorySchemOut({
            'status': EditHistorySchemOut.STATUS_ERROR,
            'error': EditHistorySchemOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(edit_history_schema_out.to_native(), status=400)

    comment = Comment.objects.filter(
        id=edit_history_schema_in.comment_id
    ).first()
    if not comment:
        edit_history_schema_out = EditHistorySchemOut({
            'status': EditHistorySchemOut.STATUS_ERROR,
            'error': EditHistorySchemOut.ERROR_COMMENT_NOT_FOUND,
        })
        return JsonResponse(edit_history_schema_out.to_native(), status=400)

    edit_history = [
        version._object_version.object.to_dict()
        for version in Version.objects.get_for_object(
            comment).order_by('revision__date_created')
    ]

    edit_history_schema_out = EditHistorySchemOut({
        'status': EditHistorySchemOut.STATUS_OK,
    })
    result = edit_history_schema_out.to_native()
    result['edit_history'] = edit_history
    return JsonResponse(result)
