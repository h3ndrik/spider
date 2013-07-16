#!/usr/bin/env python3
# coding: utf-8

import logging
import os, signal
import sys
from mediaspider.helper import parse_args
from mediaspider.db import DB
from mediaspider.models import Control, Files
from mediaspider.fs import FS
from mediaspider import __version__

logger = logging.getLogger(__name__)

"""
    spider
    ~~~~~~~~~
    
    Crawl ...
        
    :copyleft: 2013 by h3ndrik.
    :license: WTFTPL, see LICENSE for more details.
"""

def interrupthandler(signum, frame):
    logger.warning("Caught Interrupt: " + signum)
    sys.exit(0)

def main():
    # Startup
    if sys.version_info <= (3, 0):
        logger.error('This program will not work with python2')
        sys.exit(1)
    os.nice(19)
    # Set up handlers for signals
    signal.signal(signal.SIGINT, interrupthandler)
    signal.signal(signal.SIGTERM, interrupthandler)
    args = parse_args()

    crawler = Crawler(args.database)

    logger.info("=== Spider v." + repr(__version__) + " ===")
    if os.geteuid() == 0:
        logger.warning("Warning, running as root")

    #args.func(args)  # Broken, work around:
#    print args
    if args.sub == 'add':
        crawler.add(args)
    elif args.sub == 'del':
        crawler.delete(args)
    elif args.sub == 'disable':
        crawler.disable(args)
    elif args.sub == 'enable':
        crawler.enable(args)
    elif args.sub == 'crawl':
        crawler.crawl(args)
    elif args.sub == 'meta':
        crawler.meta(args)
    elif args.sub == 'list':
        crawler.list(args)
    else:
        crawler.crawl(args)

    logger.info("Done. Exiting.")

if __name__ == '__main__':
    main()

class Crawler:
    """mislabeled main program"""

    def __init__(self, database='sqlite:///spider.db'):
        self.db = DB(database=database)
        pass

    def __del__(self):
        pass

    def add(self, args):
        """add name directory mountpoint"""
        item = Control(args.name, args.directory, args.mountpoint, args.hash)
        self.db.add(item)
        self.db.session.commit()
    def delete(self, args):
        """del name"""
        item = self.db.getControl(args.name)
        self.db.delete(item)
        self.db.session.commit()
    def disable(self, args):
        """disable name"""
        item = self.db.getControl(args.name)
        if item.crawl == 0:
            logger.info('Already disabled')
        item.crawl = 0
        self.db.session.commit()
    def enable(self, args):
        """enable name"""
        item = self.db.getControl(args.name)
        if item.crawl == 1:
            logger.info('Already enabled')
        item.crawl = 1
        self.db.session.commit()
    def list(self, args):
        """list"""
        for item in self.db.session.query(Control):
            print("Name: \"" + item.name + "\", Directory: \"" + item.directory + "\", NeedsMointpoint: \"" + item.needsmountpoint + "\", Enabled: " + str(item.crawl) + ", Hash: " + item.hashalgorithm)
    def crawl(self, args):
        """crawl"""
        if hasattr(args, "name"):
            items = self.db.getJobs(args.name)
        else:
            items = self.db.getJobs()
        for item in items:
            logger.info('Starting crawl of: ' + item.name)
            if hasattr(args, "hash") and args.hash:
                hashalgorithm = args.hash
                logger.info('User selected hash-method: ' + args.hash)
                if not args.hash == item.hashalgorithm:
                    logger.warning('Selected hash-algorithm does not match configured one')
            else:
                hashalgorithm = item.hashalgorithm
            if hasattr(args, 'nometa') and args.nometa == True:
                metacrawl = False
            else:
                metacrawl = True
            try:
                self.check(item.name)
                self.db.lock(item)
                fs = FS(self.db, item, hashalgorithm, metacrawl)
                fs.walk()
                self.db.unlock(item)
            except CrawlerError:
                pass
            except:
                self.db.session.rollback()
                item.errors += 1
                self.db.session.commit()
                self.db.unlock(item)
                raise

    def meta(self, args):
        """update metadata"""
        if hasattr(args, "name"):
            items = self.db.getJobs(args.name)
        else:
            items = self.db.getJobs()
        for item in items:
            logger.info('Getting Metadata of: ' + item.name)
            try:
                self.check(item.name)
                self.db.lock(item)
                fs = FS(self.db, item)
                fs.updatemeta()
                self.db.unlock(item)
            except CrawlerError:
                pass
            except:
                self.db.session.rollback()
                item.errors += 1
                self.db.session.commit()
                self.db.unlock(item)
                raise

    def check(self, name):
        """check if it's safe to crawl 'name'"""
        item = self.db.getControl(name)
        if item.crawl != 1:
            logger.warning('Directory marked not to crawl. Skipping.')
            raise(CrawlerError('Directory marked not to crawl. Skipping.'))
        if item.pid_lock != 0:
            try:
                os.kill(item.pid_lock, 0)	# Sends nothing but raises exception if pid is not valid
            except OSError:
                logger.warning('Last crawl did not terminate cleanly. Proceeding.')
                item.pid_lock = 0
                self.db.session.commit()
            else:
                logger.error('Another crawl is running simultaneously. Skipping.')
                raise(CrawlerError('Another crawl is running simultaneously. Skipping.'))
        if not os.path.ismount(item.needsmountpoint):
            logger.error('Not mounted. Needs mount point: \"' + item.needsmountpoint + '\". Aborting')
            raise(CrawlerError('Runtime error'))

class CrawlerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

