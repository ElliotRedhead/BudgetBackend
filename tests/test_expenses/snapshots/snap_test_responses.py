# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["TestExpenseResponses::test_expense_detail_response_admin 1"] = {
    "cost": "316.00",
    "date": "1986-10-10T08:04:48Z",
    "date_created": "2021-06-27T22:18:39Z",
    "date_modified": "1984-08-08T01:55:43Z",
    "id": 1,
    "name": "Utilities",
    "user": "Jesse Weiss",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 2"] = {
    "cost": "329.66",
    "date": "2009-10-19T06:09:49Z",
    "date_created": "1999-01-31T10:30:02Z",
    "date_modified": "2012-10-19T15:24:26Z",
    "id": 2,
    "name": "Utilities",
    "user": "Amanda Horton",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 3"] = {
    "cost": "817.42",
    "date": "1979-04-10T08:30:32Z",
    "date_created": "1975-07-04T09:35:08Z",
    "date_modified": "1974-12-01T22:10:39Z",
    "id": 3,
    "name": "Clothes",
    "user": "Thomas Brown",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 4"] = {
    "cost": "279.65",
    "date": "2000-06-08T20:43:52Z",
    "date_created": "1990-03-10T12:02:32Z",
    "date_modified": "1976-01-21T12:36:14Z",
    "id": 4,
    "name": "Healthcare",
    "user": "Diane Freeman",
}

snapshots["TestExpenseResponses::test_expense_detail_response_admin 5"] = {
    "cost": "469.62",
    "date": "1970-10-07T05:05:24Z",
    "date_created": "1986-05-10T02:29:06Z",
    "date_modified": "2020-02-04T22:19:21Z",
    "id": 5,
    "name": "Holiday",
    "user": "Daniel Davis",
}

snapshots["TestExpenseResponses::test_expense_detail_response_user_owned 1"] = {
    "cost": "316.00",
    "date": "2002-08-26T06:33:19Z",
    "date_created": "2000-09-22T16:08:30Z",
    "date_modified": "1971-01-20T05:05:27Z",
    "id": 1,
    "name": "Utilities",
    "user": "user",
}

snapshots["TestExpenseResponses::test_expense_list_empty_response 1"] = []

snapshots["TestExpenseResponses::test_expense_list_response_admin 1"] = [
    {
        "cost": "469.62",
        "date": "1970-10-07T05:05:24Z",
        "date_created": "1986-05-10T02:29:06Z",
        "date_modified": "2020-02-04T22:19:21Z",
        "id": 5,
        "name": "Holiday",
        "user": "Daniel Davis",
    },
    {
        "cost": "279.65",
        "date": "2000-06-08T20:43:52Z",
        "date_created": "1990-03-10T12:02:32Z",
        "date_modified": "1976-01-21T12:36:14Z",
        "id": 4,
        "name": "Healthcare",
        "user": "Diane Freeman",
    },
    {
        "cost": "817.42",
        "date": "1979-04-10T08:30:32Z",
        "date_created": "1975-07-04T09:35:08Z",
        "date_modified": "1974-12-01T22:10:39Z",
        "id": 3,
        "name": "Clothes",
        "user": "Thomas Brown",
    },
    {
        "cost": "329.66",
        "date": "2009-10-19T06:09:49Z",
        "date_created": "1999-01-31T10:30:02Z",
        "date_modified": "2012-10-19T15:24:26Z",
        "id": 2,
        "name": "Utilities",
        "user": "Amanda Horton",
    },
    {
        "cost": "316.00",
        "date": "1986-10-10T08:04:48Z",
        "date_created": "2021-06-27T22:18:39Z",
        "date_modified": "1984-08-08T01:55:43Z",
        "id": 1,
        "name": "Utilities",
        "user": "Jesse Weiss",
    },
]

snapshots["TestExpenseResponses::test_expense_list_response_user 1"] = [
    {
        "cost": "253.01",
        "date": "1974-04-07T11:12:22Z",
        "date_created": "1987-06-17T05:23:30Z",
        "date_modified": "1977-02-18T21:55:06Z",
        "id": 7,
        "name": "Clothes",
        "user": "user",
    },
    {
        "cost": "998.48",
        "date": "1981-06-13T00:55:19Z",
        "date_created": "1992-07-05T15:08:59Z",
        "date_modified": "1982-02-27T18:46:31Z",
        "id": 6,
        "name": "Holiday",
        "user": "user",
    },
]
