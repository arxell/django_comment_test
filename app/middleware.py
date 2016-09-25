import logging

from django.http.response import JsonResponse

log = logging.getLogger(__name__)


class ExceptionMiddleware(object):

    def process_exception(self, request, exception):
        log.error(
            'Somethin Went Wrong',
            exc_info=True,
        )
        return JsonResponse({'error': 'somethin_went_wrong'})
