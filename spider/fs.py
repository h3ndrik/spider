import logging
import os, sys
from time import time
import mimetypes
mimetypes.init()
from spider.db import DB
from spider.models import Control, Files, TmpFiles
from spider.helper import md5sum, nonesum
from spider.meta import Meta

class FS(object):
    """All Filesystem interaction"""

    def __init__(self, db, control, hashalgorithm='md5'):
        self.db = db
        self.control = control
        self.directory = control.directory
        self.category = control.name
        self.meta = Meta(self.db, control.name)
        self.timeout = 2592000
        if hashalgorithm == 'md5' or hashalgorithm == 'md5sum':
            self.hashsum = md5sum
        elif hashalgorithm == 'none' or hashalgorithm == 'None':
            logging.info('Not computing hashsums')
            self.hashsum = nonesum
        else:
            self.hashsum = nonesum
            raise(Exception('Hash algorithm not implemented'))

    def walk(self):
        """execute subroutines of filecrawler"""
        logging.info('Reading Filesystem')
        self.read_fs()
        logging.info('Computing new files')
        items = self.db.session.query(TmpFiles).outerjoin((Files, TmpFiles.filename == Files.filename)).\
                                                filter(Files.filename == None).\
                                                filter(Files.removed == None).all()

        logging.info('Analyzing Files')
        for item in items:
            #logging.debug('Analyzing: ' + item.filename)
            try:
                self.insertfile(item.filename)
            except:
                #TODO: insert with flag set
                logging.warning('Could not insert file. Probably bad encoding?')
                self.control.errors += 1
                self.db.session.commit()
                pass
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
        """walk filesystem and write to temporary table"""
        self.db.cleanTmpFiles()
        fs_enc = sys.getfilesystemencoding()
#        if sys.version_info <= (3, 0):
#            self.directory = unicode(self.directory, fs_enc)
        for dir, subdirs, files in os.walk(self.directory.encode(fs_enc)):
            logging.debug(''.join(["Reading dir: ", dir.decode(fs_enc, 'replace')]))
            for subdir in subdirs:
                try:
#                    if not os.path.ismount(os.path.join(dir, subdir)):
#                      logging.warning('mountpoint?')
                    filename = os.path.join(dir, subdir)
                    mtime = os.stat(filename).st_mtime
                    item = TmpFiles(filename=filename.decode(fs_enc, 'replace'), mtime=mtime)
                    self.db.add(item)
                except:
                    logging.warning(''.join(['Could not read dir: ', filename.decode(fs_enc, 'replace')]))
            for file in files:
                try:
                    filename = os.path.join(dir, file)
                    mtime = os.stat(filename).st_mtime
                    item = TmpFiles(filename=filename.decode(fs_enc, 'replace'), mtime=mtime)
                    self.db.add(item)
                except:
                    logging.warning(''.join(['Could not read file: ', filename.decode(fs_enc, 'replace')]))

            #if '.git' in subdirs:
                #TODO: prune directories
                #subdirs.remove('.git')  # don't visit .git directories
        self.db.session.commit()

    def insertfile(self, filename):
        """gather filesystem infos for 'filename' and write to table"""
        #filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            logging.debug(''.join(["Updating(New): ", filename]))
            (mime, encoding) = mimetypes.guess_type(filename)
            hash = self.hashsum(filename)
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
        """mark 'filename' as removed"""
        item = self.db.session.query(Files).filter(Files.filename == filename).one()
        item.removed = time()
