# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["TestExpenseResponses::test_expense_detail_response_admin 1"] = {
    "cost": 316,
    "date": "1985-03-22T00:52:07Z",
    "date_created": "1991-04-15T11:29:35Z",
    "date_modified": "1984-02-19T13:13:00Z",
    "id": 1,
    "name": "utilities",
    "user": "aduke@example.com",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 2"] = {
    "cost": 960,
    "date": "1988-07-12T23:29:58Z",
    "date_created": "1971-07-28T06:27:31Z",
    "date_modified": "1981-05-21T03:56:12Z",
    "id": 2,
    "name": "holiday",
    "user": "vcross@example.com",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 3"] = {
    "cost": 216,
    "date": "2002-12-15T11:34:02Z",
    "date_created": "1978-03-25T02:47:02Z",
    "date_modified": "1974-10-26T16:29:07Z",
    "id": 3,
    "name": "utilities",
    "user": "jesus06@example.net",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 4"] = {
    "cost": 10,
    "date": "1994-03-14T02:23:58Z",
    "date_created": "2020-06-19T10:51:42Z",
    "date_modified": "2013-01-13T06:23:20Z",
    "id": 4,
    "name": "groceries",
    "user": "christopherdaniels@example.net",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 5"] = {
    "cost": 792,
    "date": "1972-06-22T17:58:27Z",
    "date_created": "2015-04-01T11:39:01Z",
    "date_modified": "1992-01-19T16:00:19Z",
    "id": 5,
    "name": "transport",
    "user": "courtney22@example.org",
}

snapshots["TestExpenseResponses::test_expense_detail_response_user_owned 1"] = {
    "cost": 316,
    "date": "2002-08-26T06:33:19Z",
    "date_created": "2000-09-22T16:08:30Z",
    "date_modified": "1971-01-20T05:05:27Z",
    "id": 1,
    "name": "utilities",
    "user": "user@user.com",
}

snapshots["TestExpenseResponses::test_expense_list_empty_response 1"] = []

snapshots["TestExpenseResponses::test_expense_list_response_admin 1"] = [
    {
        "cost": 792,
        "date": "1972-06-22T17:58:27Z",
        "date_created": "2015-04-01T11:39:01Z",
        "date_modified": "1992-01-19T16:00:19Z",
        "id": 5,
        "name": "transport",
        "user": "courtney22@example.org",
    },
    {
        "cost": 10,
        "date": "1994-03-14T02:23:58Z",
        "date_created": "2020-06-19T10:51:42Z",
        "date_modified": "2013-01-13T06:23:20Z",
        "id": 4,
        "name": "groceries",
        "user": "christopherdaniels@example.net",
    },
    {
        "cost": 216,
        "date": "2002-12-15T11:34:02Z",
        "date_created": "1978-03-25T02:47:02Z",
        "date_modified": "1974-10-26T16:29:07Z",
        "id": 3,
        "name": "utilities",
        "user": "jesus06@example.net",
    },
    {
        "cost": 960,
        "date": "1988-07-12T23:29:58Z",
        "date_created": "1971-07-28T06:27:31Z",
        "date_modified": "1981-05-21T03:56:12Z",
        "id": 2,
        "name": "holiday",
        "user": "vcross@example.com",
    },
    {
        "cost": 316,
        "date": "1985-03-22T00:52:07Z",
        "date_created": "1991-04-15T11:29:35Z",
        "date_modified": "1984-02-19T13:13:00Z",
        "id": 1,
        "name": "utilities",
        "user": "aduke@example.com",
    },
]

snapshots["TestExpenseResponses::test_expense_list_response_user 1"] = [
    {
        "cost": 421,
        "date": "1979-10-12T11:11:26Z",
        "date_created": "2004-06-19T21:49:35Z",
        "date_modified": "1990-03-24T06:28:34Z",
        "id": 7,
        "name": "clothes",
        "user": "user@user.com",
    },
    {
        "cost": 456,
        "date": "2001-02-14T00:23:18Z",
        "date_created": "2022-02-27T23:52:18Z",
        "date_modified": "1996-12-01T00:12:48Z",
        "id": 6,
        "name": "groceries",
        "user": "user@user.com",
    },
]
