import csv
import io

from django.http.response import HttpResponse
import contracts


@contracts.contract
def _format(comments):
    """
        :type comments: list(Comment)
        :rtype: str
    """
    string = io.StringIO()
    cw = csv.writer(
        string,
        delimiter='|',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL
    )

    cw.writerow([
        'id', 'text', 'user_id', 'type_id', 'object_id',
        'modified_at', 'created_at'
    ])

    for comment in comments:
        cw.writerow([
            comment.pk, comment.text, comment.user_id, comment.type_id,
            comment.object_id,
            comment.modified_at.isoformat(), comment.created_at.isoformat()
        ])

    return string.getvalue().strip('\r\n')


class CsvResponse(HttpResponse):

    @contracts.contract
    def __init__(self, comments, data=None, filename='file', **kwargs):
        """
            :type comments: list(Comment)
        """
        if not data:
            data = _format(comments)
        kwargs.setdefault('content_type', 'text/csv')
        super(CsvResponse, self).__init__(content=data, **kwargs)
