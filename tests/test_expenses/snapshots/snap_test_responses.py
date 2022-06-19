# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestExpenseResponses.test_expense_list_response 1'] = [
    {
        'cost': '601.30',
        'date': '1988-09-10T10:46:40Z',
        'date_created': '2013-10-06T23:16:19Z',
        'date_modified': '1993-05-01T19:39:23Z',
        'id': 1,
        'name': 'Healthcare',
        'user': 'Paul Morrison'
    },
    {
        'cost': '364.82',
        'date': '1991-01-27T02:26:55Z',
        'date_created': '2011-01-20T15:11:33Z',
        'date_modified': '2019-07-27T06:59:26Z',
        'id': 3,
        'name': 'Leisure',
        'user': 'Dylan Peterson'
    },
    {
        'cost': '83.91',
        'date': '1987-01-02T15:25:12Z',
        'date_created': '2010-08-09T18:10:33Z',
        'date_modified': '1984-03-01T01:53:30Z',
        'id': 4,
        'name': 'Furniture',
        'user': 'Colleen Reid'
    },
    {
        'cost': '891.84',
        'date': '2015-01-31T12:53:27Z',
        'date_created': '1989-05-01T15:09:21Z',
        'date_modified': '2012-06-20T17:04:21Z',
        'id': 5,
        'name': 'Utilities',
        'user': 'Bridget Randall'
    },
    {
        'cost': '224.35',
        'date': '2001-01-05T01:07:27Z',
        'date_created': '1973-02-04T03:20:36Z',
        'date_modified': '1995-06-25T06:06:02Z',
        'id': 2,
        'name': 'Transport',
        'user': 'Misty Lopez'
    }
]
