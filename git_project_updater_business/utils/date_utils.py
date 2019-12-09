import datetime
import sys


def millis_to_date(millis):
    return datetime.datetime.fromtimestamp(millis).replace(microsecond=int(7100000/1000))
