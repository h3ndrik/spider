
"""timestamp2human:
from dateutil.relativedelta import relativedelta

attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
human_readable = lambda delta: [
    '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1]) 
        for attr in attrs if getattr(delta, attr)
]

human_readable(relativedelta(minutes=125))
"""

"""size2human:
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
"""
