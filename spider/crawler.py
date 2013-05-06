import logging
import os
from spider.db import DB
from spider.models import Control, Files
from spider.fs import FS

class Crawler:

    def __init__(self):
        self.db = DB()
        pass

    def __del__(self):
        pass

    def add(self, args):
        item = Control(args.name, args.directory, args.mountpoint)
        self.db.add(item)
        self.db.session.commit()
    def delete(self, args):
        item = self.db.getControl(args.name)
        self.db.delete(item)
        self.session.commit()
    def disable(self, args):
        item = self.db.getControl(args.name)
        if item.crawl == 0:
            logging.info('Already disabled')
        item.crawl = 0
        self.db.session.commit()
    def enable(self, args):
        item = self.db.getControl(args.name)
        if item.crawl == 1:
            logging.info('Already enabled')
        item.crawl = 1
        self.db.session.commit()
    def crawl(self, args):
        if hasattr(args, "name"):
            items = self.db.getJobs(args.name)
        else:
            items = self.db.getJobs()
        for item in items:
            logging.info('Starting crawl of: ' + item.name)
            try:
                self.check(item.name)
                self.db.lock(item)
                fs = FS(self.db, item.directory, item.name)
                self.db.unlock(item)
                fs.walk()
            except CrawlerError:
                pass
            except:
                item.errors += 1
                self.db.session.commit()
                raise

    def check(self, name):
        item = self.db.getControl(name)
        if item.crawl != 1:
            logger.warning('Directory marked not to crawl. Skipping.')
            raise(CrawlerError('Directory marked not to crawl. Skipping.'))
        if item.pid_lock != 0:
            try:
                os.kill(item.pid_lock, 0)
            except OSError:
                logging.warning('Last crawl did not terminate cleanly. Proceeding.')
                item.pid_lock = 0
                self.db.session.commit()
            else:
                logging.error('Another crawl is running simultaneously. Skipping.')
                raise(CrawlerError('Another crawl is running simultaneously. Skipping.'))
        if not os.path.ismount(item.needsmountpoint):
            logging.error('Not mounted. Needs mount point: \"' + item.needsmountpoint + '\". Aborting')
            raise(CrawlerError('Runtime error'))

class CrawlerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

