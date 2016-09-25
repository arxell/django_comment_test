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
* /api/comment/v1/add/?type_id=1&object_id=123&text=qwe&&user_id=123
* /api/comment/v1/add/?parent_id=190272&text=qwe&user_id=826


 Table Screenshot
-------------------
![Alt text](/images/table1.png?raw=true "Table")

 Load Page Time
---------------------
2016-08-28 12:20:11,031 DEBUG app.utils _get_history_deals_data 0.017056941986083984 (sec)

2016-08-28 12:20:11,046 DEBUG app.utils _get_history_deposit_data 0.01406407356262207 (sec)

2016-08-28 08:00:50,236 DEBUG app.utils view 2.395364046096802 (sec)

