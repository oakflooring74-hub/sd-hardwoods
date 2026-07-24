# -*- coding: utf-8 -*-
"""US Pacific Time UTC offset, stdlib-only (no tzdata package required).

DST rule in effect since 2007: starts 2nd Sunday in March, ends 1st Sunday
in November. Used to give schema.org uploadDate values a real UTC offset
(Google's Video structured-data guidance expects one) without adding an
external timezone-database dependency to the stdlib-only build pipeline.
"""
from datetime import date, timedelta


def _nth_sunday(year, month, n):
    d = date(year, month, 1)
    first_sunday = d + timedelta(days=(6 - d.weekday()) % 7)
    return first_sunday + timedelta(weeks=n - 1)


def pacific_offset(d):
    dst_start = _nth_sunday(d.year, 3, 2)
    dst_end = _nth_sunday(d.year, 11, 1)
    return "-07:00" if dst_start <= d < dst_end else "-08:00"


def to_pacific_iso(date_str, time_str="00:00:00"):
    y, m, dd = (int(x) for x in date_str.split("-"))
    return f"{date_str}T{time_str}{pacific_offset(date(y, m, dd))}"
