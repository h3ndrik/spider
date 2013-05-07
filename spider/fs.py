import logging
import os, sys
from time import time
import mimetypes
mimetypes.init()
from spider.db import DB
from spider.models import Control, Files, TmpFiles
from spider.helper import hashsum
from spider.meta import Meta

class FS(object):

    def __init__(self, db, directory, name):
        self.db = db
        self.directory = directory
        self.category = name
        self.meta = Meta(self.db, name)
        self.timeout = 2592000

    def walk(self):
        logging.info('Reading Filesystem')
        self.read_fs()
        logging.info('Computing new files')
        items = self.db.session.query(TmpFiles).outerjoin((Files, TmpFiles.filename == Files.filename)).\
                                                filter(Files.filename == None).\
                                                filter(Files.removed == None).all()

        logging.info('Analyzing Files')
        for item in items:
            logging.debug('Analyzing: ' + item.filename)
            self.insertfile(item.filename)
        self.db.session.commit()

        logging.info('Computing deleted files')
        items = self.db.session.query(Files).outerjoin((TmpFiles, Files.filename == TmpFiles.filename)).\
                                                filter(TmpFiles.filename == None).\
                                                filter(Files.removed == None).all()
        logging.info('Removing')
        for item in items:
            logging.debug('Removing: ' + item.filename)
            self.removefile(item.filename)
        self.db.session.commit()

        #logging.info('Deleting old database entries')
        # TODO and think of meta table

    def read_fs(self):
        self.db.cleanTmpFiles()
        fs_enc = sys.getfilesystemencoding()
#        if sys.version_info <= (3, 0):
#            self.directory = unicode(self.directory, fs_enc)
        for dir, subdirs, files in os.walk(self.directory):
            logging.debug(''.join(["Reading dir: ", dir]))
            for subdir in subdirs:
                filename = os.path.join(dir, subdir)
                mtime = os.stat(filename).st_mtime
                item = TmpFiles(filename=filename, mtime=mtime)
                self.db.add(item)
            for file in files:
                filename = os.path.join(dir, file)
                mtime = os.stat(filename).st_mtime
                item = TmpFiles(filename=filename, mtime=mtime)
                self.db.add(item)

            #if '.git' in subdirs:
                #TODO: prune directories
                #subdirs.remove('.git')  # don't visit .git directories
        self.db.session.commit()

    def insertfile(self, filename):
        #filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            logging.debug(''.join(["Updating(New): ", filename]))
            (mime, encoding) = mimetypes.guess_type(filename)
            hash = hashsum(filename)
            removed = None
        elif os.path.isdir:
            logging.debug(''.join(["Updating(New,Dir): ", filename]))
            mime = "directory"
            hash = None
            removed = None
        else:
            logging.debug(''.join(["Updating(Removed): ", filename]))
            removed = time()
            pass # TODO!

        filestat = os.stat(filename)
        mtime = filestat.st_mtime
        firstseen = time()
        size = filestat.st_size
        category = self.category

        removed = None
        item = Files(filename=filename, category=category, mtime=mtime, firstseen=firstseen, size=size, mime=mime, hash=hash, removed=removed)
        self.db.add(item)
        self.db.session.flush()
        self.meta.insertmeta(filename, item.id)

    def removefile(self, filename):
        item = self.db.session.query(Files).filter(Files.filename == filename).one()
        item.removed = time()
