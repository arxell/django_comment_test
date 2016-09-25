import logging

from django.http.response import JsonResponse
from schematics.exceptions import ModelConversionError, ValidationError

from app.comment.defs import ExportSchemaIn, ExportSchemaOut
from app.export import XmlResponse, CsvResponse
from app.comment.models import Comment, Export
from app.utils import timeit


log = logging.getLogger(__name__)


@timeit
def view(request):
    """
    View for /api/comment/v1/export

    Input Schema:
        ExportSchemaIn
    Output Schema:
        ExportSchemaOut

    Examples:
        /api/comment/v1/export/?user_id=1&created_at_from=2016-09-23T06:25:04.189753&format=cvs
    """
    try:
        export_in = ExportSchemaIn(
            request.GET.dict()
        )
    except (ValidationError, ModelConversionError) as exp:
        export_out = ExportSchemaOut({
            'status': ExportSchemaOut.STATUS_ERROR,
            'error': ExportSchemaOut.ERROR_INVALID_INPUT_DATA,
            'error_extra': str(exp),
        })
        return JsonResponse(export_out.to_native(), status=400)

    if export_in.user_id:
        # by user_id
        query = Comment.objects.filter(
            user_id=export_in.user_id
        )

    if export_in.type_id and export_in.object_id:
        # by type_id/object_id
        query = Comment.objects.filter(
            type_id=export_in.type_id,
            object_id=export_in.object_id,
        )

    if export_in.created_at_from:
        query = query.filter(
            created_at__gte=export_in.created_at_from
        )
    if export_in.created_at_to:
        query = query.filter(
            created_at__lte=export_in.created_at_to
        )
    comments = list(query.order_by('created_at'))

    if export_in.is_csv_format:
        response = CsvResponse(comments)
        response['Content-Disposition'] = 'attachment; filename="user_history.csv"'
    elif export_in.is_xml_format:
        response = XmlResponse(comments)
        response['Content-Disposition'] = 'attachment; filename="user_history.xml"'
    else:
        response = JsonResponse([c.to_dict() for c in comments], safe=False)
        response['Content-Disposition'] = 'attachment; filename="user_history.json"'

    export = Export.objects.create(user_id=export_in.user_id)
    export.set_data(response)
    export.save(update_fields=['data'])

    return response
