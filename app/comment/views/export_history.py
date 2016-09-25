import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.defs import ExportHistorySchemaIn, ExportHistorySchemaOut
from app.comment.models import Export
from app.utils import timeit


log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/export/history

    Input Schema:
        ExportHistorySchemaIn
    Output Schema:
        ExportHistorySchemaOut

    Examples:
        /api/comment/v1/export/history?user_id=1
    """
    try:
        export_history_in = ExportHistorySchemaIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        export_history_out = ExportHistorySchemaOut({
            'status': ExportHistorySchemaOut.STATUS_ERROR,
            'error': ExportHistorySchemaOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(export_history_out.to_native(), status=400)

    export_history_out = ExportHistorySchemaOut({
        'status': ExportHistorySchemaOut.STATUS_OK,
    })
    result = export_history_out.to_native()

    user_export_history = [
        {
            'id': export.id,
            'user_id': export.user_id,
            'created_at': export.created_at.isoformat(),
        }
        for export in Export.objects.filter(user_id=export_history_in.user_id)
    ]
    result['user_export_history'] = user_export_history

    return JsonResponse(result)
