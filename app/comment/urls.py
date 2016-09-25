from django.conf.urls import url

from .views import add
from .views import edit
from .views import edit_history
from .views import delete
from .views import tree
from .views import user_history
from .views import export
from .views import export_history
from .views import export_restore


urlpatterns = [
    url(r'^v1/add/?$', add.view),
    url(r'^v1/edit/?$', edit.view),
    url(r'^v1/edit/history?$', edit_history.view),
    url(r'^v1/delete/?$', delete.view),
    url(r'^v1/tree/?$', tree.view),
    url(r'^v1/user/history/?$', user_history.view),
    url(r'^v1/export/?$', export.view),
    url(r'^v1/export/history?$', export_history.view),
    url(r'^v1/export/restore?$', export_restore.view),
]
