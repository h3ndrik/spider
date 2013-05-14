import logging
import hashlib
import argparse
import os
from configparser import SafeConfigParser

from time import time
from datetime import timedelta

logger = logging.getLogger(__name__)

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
    logger = logging.getLogger(__name__)
    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument("-c", "--conf_file",
                             help="Specify config file", metavar="FILE", default='spider.conf')
    args, remaining_argv = conf_parser.parse_known_args()
    defaults = {
        'database' : 'sqlite:///spider.db',
        'loglevel' : 'INFO',
        'logfile' : '',
        }

    """Config file format:
    [Spider]
    database = sqlite:///spider.db
    # database = mysql://user:pass@localhost/database
    loglevel = INFO
    logfile = spider.log
    [WebUI]
    title = Spider Search
    host = 0.0.0.0
    # host = localhost
    port = 8080
    debug = False
    [datapath_substitutions]
    /media/videos = ftp://192.168.1.2/pub/videos
    /media/audio = /file/audio
    """

    # read global config
    search_path = ['/etc', '']
    for path in search_path:
        candidate = os.path.join(path, 'spider.conf')
        if os.path.isfile(candidate):
            logger.info('Reading global conffile ' + candidate)
            config = SafeConfigParser()
            config.read([candidate])
            defaults.update(dict(config.items('Spider')))

    if args.conf_file and os.path.isfile(args.conf_file):
        logger.info('Reading conffile(2) ' + args.conf_file)
        config = SafeConfigParser()
        config.read([args.conf_file])
        #defaults['verbose'] = config.getint('Spider', 'verbose')
        #defaults['database'] = config.get('Spider', 'database')
        defaults.update(dict(config.items('Spider')))

    parser = argparse.ArgumentParser(description='Crawl filesystem.',
                                     parents=[conf_parser])
    parser.add_argument("-v", "--verbose", action="count", default=0,
                    help="increase output verbosity")
    parser.add_argument("--database", help="specify database path")
    parser.set_defaults(**defaults)

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
    #parser_del.set_defaults(func=delete)

    parser_disable = subparsers.add_parser('disable', help='temporarily remove directory from crawl')
    parser_disable.add_argument('name',
                   help='name')
    #parser_disable.set_defaults(func=disable)

    parser_enable = subparsers.add_parser('enable', help='enable crawl of directory')
    parser_enable.add_argument('name',
                   help='name')
    #parser_enable.set_defaults(func=enable)

    parser_crawl = subparsers.add_parser('crawl', help='start a single crawl')
    parser_crawl.add_argument('--name',
                   help='only crawl name')
    parser_crawl.add_argument("--hash",
                   help="specify hash algorithm or \'none\'")
    parser_crawl.add_argument("--nometa", action='store_true',
                   help="do not get meta information")
    #parser_crawl.set_defaults(func=crawl)

    parser_meta = subparsers.add_parser('meta', help='only update metadata')
    parser_meta.add_argument('--name',
                   help='only update name')
    #parser_meta.set_defaults(func=meta)

    parser_list = subparsers.add_parser('list', help='list configured directories')
    #parser_list.set_defaults(func=list)

    args = parser.parse_args(remaining_argv)

    logger = logging.getLogger()

    if int(args.verbose) >= 3:
        logging.basicConfig(level=logging.DEBUG)  # Log everything, and send it to stderr.
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug output enabled")
    elif int(args.verbose) >= 2:
        logging.basicConfig(level=logging.INFO)  # Log everything, and send it to stderr.
        logger.setLevel(logging.INFO)
    elif int(args.verbose) >= 1:
        logging.basicConfig(level=logging.WARNING)  # Log everything, and send it to stderr.
        logger.setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=logging.ERROR)  # Log everything, and send it to stderr.
        logger.setLevel(logging.ERROR)

    if not args.logfile == '':
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.basicConfig(filename=args.logfile, level=numeric_level)
        logger.addHandler(logging.FileHandler(args.logfile))

    return args
