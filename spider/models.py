from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Control(Base):
    """"""
    __tablename__ = 'control'

    name = Column(String, primary_key=True)
    directory = Column(String)
    crawl = Column(Integer)
    needsmountpoint = Column(String)
    errors = Column(Integer)
    last_crawl = Column(Integer(10))
    pid_lock = Column(Integer)

    def __init__(self, name, directory, needsmountpoint):
        self.name = name
        self.directory = directory
        self.needsmountpoint = needsmountpoint
        self.crawl = 1
        self.errors = 0
        self.last_crawl = 0
        self.pid_lock = 0

    def __repr__(self):
        return "<Control('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.name, self.directory, self.needsmountpoint, self.crawl, self.errors, self.last_crawl, self.pid_lock)


class Files(Base):
    """"""
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String)
    category = Column(String)
    mtime = Column(Integer(10))
    firstseen = Column(Integer(10))
    size = Column(Integer(19))
    mime = Column(String)
    hash = Column(String(32))
    removed = Column(Integer(10))
    meta = relationship("Metadata", uselist=False, backref="files")

class Metadata(Base):
    """"""
    __tablename__ = 'meta'

    id = Column(Integer, ForeignKey('files.id'),  primary_key=True)
    #id = Column(Integer, primary_key=True)
    filetype = Column(String)
    seriesname = Column(String)
    seasonnumber = Column(Integer)
    episodenumber = Column(Integer)
    #episodenumberstart = Column(Integer)
    #episodenumberend = Column(Integer)
    #year = Column(Integer)
    #month = Column(Integer)
    #day = Column(Integer)
    duration = Column(Integer)
    resolution = Column(String)
    codec = Column(String)
    #bitrate = Column(String)
    quality = Column(String)
    group = Column(String)

    title = Column(String)
    artist = Column(String)
    album = Column(String)
    year = Column(Integer)
    track = Column(Integer)
    genre = Column(String)
    collection = Column(String)

    tags = Column(String)
    comment = Column(String)
    auto = Column(Integer)
    flag = Column(Integer)

class TmpFiles(Base):
    """"""
    __tablename__ = 'tmp'

    filename = Column(String, primary_key=True)
    mtime = Column(Integer(10))
