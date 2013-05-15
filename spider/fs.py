import logging
import os, sys
from time import time
import mimetypes
mimetypes.init()
from spider.db import DB
from spider.models import Control, Files, TmpFiles, Metadata
from spider.helper import md5sum, nonesum
from spider.meta import Meta

logger = logging.getLogger(__name__)

class FS(object):
    """All Filesystem interaction"""

    def __init__(self, db, control, hashalgorithm='md5', metacrawl=True):
        self.db = db
        self.control = control
        self.directory = control.directory
        self.category = control.name
        self.meta = Meta(self.db, control.name)
        self.metacrawl = metacrawl
        self.timeout = 2592000
        if hashalgorithm == 'md5' or hashalgorithm == 'md5sum':
            self.hashsum = md5sum
        elif hashalgorithm == 'none' or hashalgorithm == 'None':
            logger.info('Not computing hashsums')
            self.hashsum = nonesum
        else:
            self.hashsum = nonesum
            raise(Exception('Hash algorithm not implemented'))

    def walk(self):
        """execute subroutines of filecrawler"""
        logger.info('Reading Filesystem')
        self.read_fs()
        logger.info('Computing new files')
################################# TODO Repair join!!! ###########################
        items = self.db.session.query(TmpFiles).outerjoin((Files, TmpFiles.filename == Files.filename)).\
                                                filter(Files.filename == None).\
                                                filter(Files.removed == None).all()

        logger.info('Analyzing Files')
        for item in items:
            #logger.debug('Analyzing: ' + item.filename)
            try:
                self.insertfile(item.filename)
            except (getattr(__builtins__,'FileNotFoundError', IOError), OSError):
                #TODO: insert with flag set
                logger.warning('Could not insert file \'%s\'. Probably bad encoding?' % item.filename)
                self.control.errors += 1
                self.db.session.commit()
                pass
        self.db.session.commit()

        logger.info('Computing deleted files')
################################# TODO Repair join!!! ###########################
        items = self.db.session.query(Files).filter(Files.category == self.category).\
                                             outerjoin((TmpFiles, Files.filename == TmpFiles.filename)).\
                                                filter(TmpFiles.filename == None).\
                                                filter(Files.removed == None).all()
        logger.info('Removing')
        logger.warning('Not implemented')  # TODO Fix join
        for item in items:
            logger.debug('Removing: ' + item.filename)
            self.removefile(item.filename)
        self.db.session.commit()

        #logger.info('Deleting old database entries')
        # TODO and think of meta table

    def updatemeta(self):
        """update metadata"""
        logger.info('Dumping current metadata table')
        rows = self.db.session.query(Metadata).filter(Metadata.file.has(Files.category == self.category)).\
                                               filter(Metadata.auto == True).all()
        for row in rows:
            self.db.session.delete(row)
        #self.db.session.commit()
        logger.info('Updating Metadata')
        items = self.db.session.query(Files).filter(Files.category == self.category).all()
        for item in items:
            logger.debug('Updating Metadata of: ' + item.filename)
            self.meta.insertmeta(item.filename, item.id)
        self.db.session.commit()

    def read_fs(self):
        """walk filesystem and write to temporary table"""
        self.db.cleanTmpFiles()
        fs_enc = sys.getfilesystemencoding()
        if fs_enc != 'utf-8':
            logger.warning('Filesystem-encoding is not UTF-8!')
#        if sys.version_info <= (3, 0):
#            self.directory = unicode(self.directory, fs_enc)
        if isinstance(self.directory, bytes):
            self.directory = self.directory.decode('utf-8', 'surrogateescape')    # ensure unicode
        for dir, subdirs, files in os.walk(self.directory):
            logger.debug(''.join(["Reading dir: ", dir]))
            for subdir in subdirs:
                try:
#                    if not os.path.ismount(os.path.join(dir, subdir)):
#                      logger.warning('mountpoint?')
                    filename = os.path.join(dir, subdir)
                    mtime = os.stat(filename).st_mtime
                    item = TmpFiles(filename=filename.encode('utf-8', 'replace').decode('utf-8', 'strict'), mtime=mtime)
                    self.db.add(item)
                except (getattr(__builtins__,'FileNotFoundError', IOError), OSError):
                    logger.warning(''.join(['Could not read dir: ', filename]))
            for file in files:
                try:
                    filename = os.path.join(dir, file)
                    mtime = os.stat(filename).st_mtime
                    item = TmpFiles(filename=filename.encode('utf-8', 'replace').decode('utf-8', 'strict'), mtime=mtime)
                    self.db.add(item)
                except (getattr(__builtins__,'FileNotFoundError', IOError), OSError):
                    logger.warning(''.join(['Could not read file: ', filename]))

            #if '.git' in subdirs:
                #TODO: prune directories
                #subdirs.remove('.git')  # don't visit .git directories
        self.db.session.commit()

    def insertfile(self, filename):
        """gather filesystem infos for 'filename' and write to table"""
        #filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            logger.debug(''.join(["Updating(New): ", filename]))
            (mime, encoding) = mimetypes.guess_type(filename)
            hash = self.hashsum(filename)
            removed = None
            filestat = os.stat(filename)
            mtime = filestat.st_mtime
            firstseen = time()
            size = filestat.st_size
            category = self.category
        elif os.path.isdir(filename):
            logger.debug(''.join(["Updating(New,Dir): ", filename]))
            mime = "directory"
            hash = None
            removed = None
            filestat = os.stat(filename)
            mtime = filestat.st_mtime
            firstseen = time()
            size = filestat.st_size
            category = self.category
        else:
            logger.debug(''.join(["Updating(Could not read): ", filename])) # Probably due to encoding
            mime = None
            hash = None
            removed = time()
            mtime = None
            firstseen = time()
            size = None
            category = self.category

        item = Files(filename=filename, category=category, mtime=mtime, firstseen=firstseen, size=size, mime=mime, hash=hash, removed=removed)
        self.db.add(item)
        self.db.session.flush()
        if self.metacrawl:
            self.meta.insertmeta(filename, item.id)

    def removefile(self, filename):
        """mark 'filename' as removed"""
        item = self.db.session.query(Files).filter(Files.filename == filename).one()
        item.removed = time()
