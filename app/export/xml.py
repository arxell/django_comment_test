from django.http.response import HttpResponse
import contracts
import dicttoxml


@contracts.contract
def _format(comments):
    """
        :type comments: list(Comment)
        :rtype: str
    """
    data = [comment.to_dict() for comment in comments]
    xml = dicttoxml.dicttoxml(data)
    return xml.decode('utf8')


class XmlResponse(HttpResponse):

    @contracts.contract
    def __init__(self, comments, data=None, **kwargs):
        """
            :type comments: list(Comment)
        """
        if not data:
            data = _format(comments)
        kwargs.setdefault('content_type', 'application/xml')
        super(XmlResponse, self).__init__(content=data, **kwargs)
