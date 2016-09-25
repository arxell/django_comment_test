import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.defs import UserHistorySchemaIn, UserHistorySchemaOut
from app.comment.logic import user_history
from app.export import XmlResponse, CsvResponse
from app.utils import timeit

log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/user/history

    Input Schema:
        UserHistorySchemaIn
    Output Schema:
        UserHistorySchemaOut

    Examples:
        /api/comment/v1/user/history/?user_id=1&created_at_from=2016-09-23T06:25:04.189753&format=cvs
    """
    try:
        user_history_schema_in = UserHistorySchemaIn(
            request.GET.dict()
        )
    except (ValidationError, ModelConversionError) as exp:
        user_history_schema_out = UserHistorySchemaOut({
            'status': UserHistorySchemaOut.STATUS_ERROR,
            'error': UserHistorySchemaOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(user_history_schema_out.to_native(), status=400)

    user_history_schema_out, history = user_history(
        user_history_schema_in
    )

    result = user_history_schema_out.to_native()
    if user_history_schema_out.is_status_ok:
        if user_history_schema_in.is_csv_format:
            response = CsvResponse(history)
            response['Content-Disposition'] = 'attachment; filename="user_history.csv"'
            return response
        elif user_history_schema_in.is_xml_format:
            response = XmlResponse(history)
            response['Content-Disposition'] = 'attachment; filename="user_history.xml"'
            return response
        else:
            result['history'] = history
            return JsonResponse(result)
    else:
        return JsonResponse(result, status=409)
