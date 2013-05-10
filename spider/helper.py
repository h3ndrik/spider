import logging
import hashlib
import argparse

from time import time
from datetime import timedelta

def timestamp2human(timestamp):
    delta = time() - timestamp
    attrs = {'a':365.25*86400, 'd':86400, 'h':3600, 'min':60, 's':1}
    if delta < 0:
        delta = 0 - delta
        suffix = 'ahead'
    else:
        suffix = 'ago'
    output = ''
    for key in sorted(attrs, key=attrs.get, reverse=True):
        i = int(delta // attrs[key])
        delta %= attrs[key]
        if output == '':
            if i > 1:
                output = str(i) + key
        else:
            output = output + ' ' + str(i) + key
            return output + ' ' + suffix
    return output + ' ' + suffix

def size2human(num):
    for x in ['B','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


def md5sum(filename, blocksize=65536):
    h = hashlib.md5()
    f = open(filename, 'rb', encoding=None)
    buf = f.read(blocksize)
    while len(buf) > 0:
        h.update(buf)
        buf = f.read(blocksize)
    return h.hexdigest()

def nonesum(filename, blocksize=65536):
    return None

def parse_args():
    """
    Parse cmdline args
    """
    parser = argparse.ArgumentParser(description='Crawl filesystem.')
    parser.add_argument("-v", "--verbose", action="count", default=0,
                    help="increase output verbosity")
    #parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(dest='sub', help='')

    parser_add = subparsers.add_parser('add', help='add directory to crawl')
    parser_add.add_argument('name',
                   help='name to display as category')
    parser_add.add_argument('directory',
                   help='directory to crawl')
    parser_add.add_argument('mountpoint',
                   help='only crawl if mountpoint is mounted')
    parser_add.add_argument("--hash", default="md5",
                   help="specify hash algorithm or \'none\'")
    #parser_add.set_defaults(func=add)

    parser_del = subparsers.add_parser('del', help='remove directory from crawl')
    parser_del.add_argument('name',
                   help='name to display as category')
    #parser_del.add_argument('directory',
    #               help='directory to crawl')
    #parser_del.add_argument('mountpoint',
    #               help='only crawl if mountpoint is mounted')
    #parser_add.set_defaults(func=delete)

    parser_disable = subparsers.add_parser('disable', help='temporarily remove directory from crawl')
    parser_disable.add_argument('name',
                   help='name')
    #parser_add.set_defaults(func=disable)

    parser_enable = subparsers.add_parser('enable', help='enable crawl of directory')
    parser_enable.add_argument('name',
                   help='name')
    #parser_add.set_defaults(func=enable)

    parser_crawl = subparsers.add_parser('crawl', help='start a single crawl')
    parser_crawl.add_argument('--name',
                   help='only crawl name')
    parser_crawl.add_argument("--hash",
                   help="specify hash algorithm or \'none\'")
    #parser_add.set_defaults(func=crawl)

    parser_crawl = subparsers.add_parser('list', help='list configured directories')
    #parser_add.set_defaults(func=list)

    args = parser.parse_args()

    logger = logging.getLogger()

    if args.verbose >= 3:
        logging.basicConfig(level=logging.DEBUG)  # Log everything, and send it to stderr.
        logger.setLevel(logging.DEBUG)
        logging.debug("Debug output enabled")
    elif args.verbose >= 2:
        logging.basicConfig(level=logging.INFO)  # Log everything, and send it to stderr.
        logger.setLevel(logging.INFO)
    elif args.verbose >= 1:
        logging.basicConfig(level=logging.WARNING)  # Log everything, and send it to stderr.
        logger.setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=logging.ERROR)  # Log everything, and send it to stderr.
        logger.setLevel(logging.ERROR)

#    print args.accumulate(args.integers)
    return args
