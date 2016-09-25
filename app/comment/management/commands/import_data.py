import logging
import random
import string

from django.conf import settings
from django.core.management.base import BaseCommand

from app.comment.models import Comment

log = logging.getLogger(__name__)


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

USER_IDS = list(range(1, 100))
OBJECT_IDS = list(range(1, 1000))

COMMENTS_FOR_OBJECTS_NUMBER = 1000
COMMENTS_FOR_COMMENTS_NUMBER = 100000


class Command(BaseCommand):

    def handle(self, *args, **options):

        for i in range(0, COMMENTS_FOR_OBJECTS_NUMBER):
            Comment.objects.create(
                object_id=random.choice(OBJECT_IDS),
                parent=None,
                text=random_string(),
                type_id=random.choice(settings.COMMENT_TYPES_LIST),
                user_id=random.choice(USER_IDS)
            )

        parents_ids = list(Comment.objects.all().values_list('id', flat=True))
        for i in range(0, COMMENTS_FOR_COMMENTS_NUMBER):
            comment = Comment.objects.create(
                text=random_string(),
                parent_id=random.choice(parents_ids),
                user_id=random.choice(USER_IDS)
            )
            parents_ids.append(comment.id)
