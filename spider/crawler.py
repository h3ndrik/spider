import logging
import os
from spider.db import DB
from spider.models import Control, Files
from spider.fs import FS

logger = logging.getLogger(__name__)

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

