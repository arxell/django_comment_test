# Django Comment Test

API Urls
=============
* /api/comment/v1/add/
* /api/comment/v1/edit/
* /api/comment/v1/delete/
* /api/comment/v1/tree/
* /api/comment/v1/user/history/
* /api/comment/v1/export/
* /api/comment/v1/export/history/
* /api/comment/v1/export/restore/



Add Comment Examples
---------------------
* /api/comment/v1/add/?type_id=1&object_id=123&text=qwe&&user_id=123
* /api/comment/v1/add/?parent_id=190272&text=qwe&user_id=826

Edit Comment Examples
---------------------
* /api/comment/v1/edit/?comment_id=1&text=123qweasd&user_id=9272

Edit History Examples
---------------------
*  /api/comment/v1/edit/history?comment_id=238925

Delete Comment Examples
---------------------
* /api/comment/v1/delete/?comment_id=8262&user_id=282

Tree Examples
---------------------
* /api/comment/v1/tree/?comment_id=1
* /api/comment/v1/tree/?user_id=1
* /api/comment/v1/tree/?type_id=1&object_id=123

User History
---------------------
* /api/comment/v1/user/history/?user_id=1&created_at_from=2016-09-23T06:25:04.189753

Export
---------------------
* /api/comment/v1/export/?user_id=1&created_at_from=2016-09-23T06:25:04.189753&format=cvs
* /api/comment/v1/export/?type_id=1&object_id=323&format=xml

Export History
---------------------
* /api/comment/v1/export/history?user_id=1

Export Restore
---------------------
*  /api/comment/v1/export/restore?export_id=1
