import logging

from django.http.response import JsonResponse, HttpResponseBase
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.defs import ExportRestoreSchemaIn, ExportRestoreSchemaOut
from app.comment.models import Export
from app.utils import timeit


log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/export/restore

    Input Schema:
        ExportRestoreSchemaIn
    Output Schema:
        ExportHistorySchemaOut

    Examples:
        /api/comment/v1/export/restore?export_id=1
    """
    try:
        restore_in = ExportRestoreSchemaIn(request.GET.dict())
    except (ValidationError, ModelConversionError) as exp:
        export_history_out = ExportRestoreSchemaOut({
            'status': ExportRestoreSchemaOut.STATUS_ERROR,
            'error': ExportRestoreSchemaOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(export_history_out.to_native(), status=400)

    export = Export.objects.filter(id=restore_in.export_id).first()
    if not export:
        export_history_out = ExportRestoreSchemaOut({
            'status': ExportRestoreSchemaOut.STATUS_ERROR,
            'error': ExportRestoreSchemaOut.ERROR_EXPORT_NOT_FOUND,
        })
        return JsonResponse(export_history_out.to_native(), status=400)

    response = export.get_data()
    if not isinstance(response, HttpResponseBase):
        export_history_out = ExportRestoreSchemaOut({
            'status': ExportRestoreSchemaOut.STATUS_ERROR,
            'error': ExportRestoreSchemaOut.ERROR_BAD_EXPORT_DUMP,
        })
        return JsonResponse(export_history_out.to_native(), status=400)

    return response
