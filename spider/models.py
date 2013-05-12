from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from collections import OrderedDict
import json

Base = declarative_base()

class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

#class BaseModel(object):
#    """Example: Movie.load(session, movie='Europa', year='1991')"""
#    @classmethod
#    def load(cls, session, **kwargs):
#        q = session.query(cls)
#        filters = [getattr(cls, field_name)==kwargs[field_name] \
#                   for field_name in kwargs]
#        return q.filter(and_(*filters)).one()
#
#    def drop(self):
#        self.session.delete(self)
#
#    def serialize(self):
#        tmp = self.__dict__.copy()
#        del tmp['_sa_instance_state']
#        return json.dumps(tmp)

class Control(Base, DictSerializable):
    """control/config structure"""
    __tablename__ = 'control'

    name = Column(String, primary_key=True)
    directory = Column(String)
    hashalgorithm = Column(String)
    crawl = Column(Integer)
    needsmountpoint = Column(String)
    errors = Column(Integer)
    last_crawl = Column(Integer(10))
    pid_lock = Column(Integer)

    def __init__(self, name, directory, needsmountpoint, hashalgorithm='md5'):
        self.name = name
        self.directory = directory
        self.hashalgorithm = hashalgorithm
        self.needsmountpoint = needsmountpoint
        self.crawl = 1
        self.errors = 0
        self.last_crawl = 0
        self.pid_lock = 0

    def __repr__(self):
        return "<Control('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.name, self.directory, self.needsmountpoint, self.hashalgorithm, self.crawl, self.errors, self.last_crawl, self.pid_lock)


class Files(Base, DictSerializable):
    """direct attributes of file"""
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

class Metadata(Base, DictSerializable):
    """indirect and user-generated attributes of file"""
    __tablename__ = 'meta'

    id = Column(Integer, ForeignKey('files.id'))
    metaid = Column(Integer, primary_key=True)
    filetype = Column(String)
    seriesname = Column(String)
    seasonnumber = Column(Integer)
    episodenumber = Column(Integer)
    #episodenumberstart = Column(Integer)
    #episodenumberend = Column(Integer)
    #year = Column(Integer)
    #month = Column(Integer)
    #day = Column(Integer)
    language = Column(String)
    duration = Column(Integer)
    resolution = Column(String)
    codec = Column(String)
    #bitrate = Column(String)
    quality = Column(String)
    group = Column(String)

    moviename = Column(String)

    title = Column(String)
    artist = Column(String)
    album = Column(String)
    year = Column(Integer)
    track = Column(Integer)
    genre = Column(String)
    collection = Column(String)

    author = Column(String)

    tags = Column(String)
    comment = Column(String)
    auto = Column(Integer)
    flag = Column(Integer)

    source = Column(String)    # who generated this metadata

class TmpFiles(Base, DictSerializable):
    """holds snapshot of filesystem for further processing"""
    __tablename__ = 'tmp'

    filename = Column(String, primary_key=True)
    mtime = Column(Integer(10))
