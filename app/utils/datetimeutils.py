import arrow
import pytz
from datetime import datetime


PRC_TZ_STR = 'Asia/Shanghai'
prc = pytz.timezone(PRC_TZ_STR)


def prc_now_dt():
    return utc_to_prc(datetime.utcnow())


def prc_now_str(fmt='%Y-%m-%d %H:%M:%S'):
    return prc_now_dt().strftime(fmt)


def utc_to_prc(value):
    """

    :param value:
    :return:
    """
    if is_naive(value):
        print('______------------ is_naive')
        value = make_aware(value, pytz.utc)
    print('--------------val', value)
    return value
    # return value.astimezone(prc)


def is_naive(value):
    """
    Determines if a given datetime.datetime is naive.

    The logic is described in Python's docs:
    http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    return value.tzinfo is None or value.tzinfo.utcoffset(value) is None


def make_aware(value, timezone):
    """
    Makes a naive datetime.datetime in a given time zone aware.
    """
    if hasattr(timezone, 'localize'):
        print('------------------has')
        # available for pytz time zones
        return timezone.localize(value, is_dst=None)
    else:
        print('------------------not has')
        # may be wrong around DST changes
        return value.replace(tzinfo=timezone)