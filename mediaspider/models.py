from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from collections import OrderedDict
import logging
import json

logger = logging.getLogger(__name__)

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
    """attributes of file"""
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
    #parent (TODO relationship Files)
    #meta = relationship("Metadata", backref='file')

class Metadata(Base, DictSerializable):
    """indirect and user-generated attributes of file"""
    __tablename__ = 'meta'

    metaid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('files.id'))
    file = relationship("Files", backref=backref('meta')) 
    lastupdated = Column(Integer)
    source = Column(String)    # who generated this metadata
    remoteid = Column(String)  # ID on 'source'
    mtype = Column(Enum('tv_series', 'movie', 'tv_movie', 'video', 'video_game'))
    cover = Column(String)
    comment = Column(String)
    flags = Column(Integer)

    # Common attributes
    duration = Column(Integer)
    language = Column(String)
    year = Column(Integer)
    release_date
#    title = Column(String)
#    alias_titles = Column(String)

    # Quality
    codec = Column(String)
    #bitrate = Column(String)
    #resolution = Column(String)
    quality = Column(String)

    #filetype = Column(String)
    seriesname = Column(String)
    seasonnumber = Column(Integer)
    episodenumber = Column(Integer)
    #episodenumberstart = Column(Integer)
    #episodenumberend = Column(Integer)

    artist = Column(String)
    album = Column(String)
    year = Column(Integer)
    track = Column(Integer)
    genre = Column(String)
    collection = Column(String)

    author = Column(String)

    tags = Column(String)

    #votes = Column(Integer)



#class MetaTVSeries(Base, DictSerializable):
#    """Metadata from thetvdb.com"""
#    __tablename__ = 'metatvseries'
#
#    meta = relationship("Metadata", backref=backref('metaid'))
#    thetvdbseriesid
#    SeriesName
#    AliasNames
#    Overview
#    FirstAired
#    Network
#
#class MetaTVEpisode(Base, DictSerializable):
#    """Metadata from thetvdb.com"""
#    __tablename__ = 'metatvepisode'
#
#    meta = relationship("Metadata", backref=backref('metaid'))
#    thetvdbeposodeid
##    Combined_episodenumber
##    Combined_season
##    DVD_chapter
##    DVD_discid
##    DVD_episodenumber
##    DVD_Season
#    Director
#    EpImgFlag
#    EpisodeName
#    EpisodeNumber
#    FirstAired
#    GuestStars
##    IMDB_ID 
#    Overview
#    ProductionCode
#    Rating
#    SeasonNumber
#    Writer
#    absolute_number
#    img_filename
#    lastupdated
#    seasonid
#    seriesid
#
#MetaMovies(Base, DictSerializable):
#    """Metadata from IMDB"""
#    __tablename__ = 'metamovies'
#
#    id = Column(Integer, ForeignKey('files.id'))
#    file = relationship("Files", backref=backref('meta'))
#
#    actors
#also_known_as
#country
#    directors
#episodes date season episode title
#film_locations
#    genres
#    imdb_id
#imdb_url
#language
#    plot
#plot_simple
#    poster
#    rated
#    rating
#rating_count
#    release_date
#runtime
#    title
##mtype
#    writers
#    year
##business
##technical
#    votes
##cast
##crew
##critics
##trivia
##quotes


class TmpFiles(Base, DictSerializable):
    """holds snapshot of filesystem for further processing"""
    __tablename__ = 'tmp'

    filename = Column(String, primary_key=True)    # convert_unicode='force', unicode_error='replace' or Column(Unicode) http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#sqlalchemy.types.String
    mtime = Column(Integer(10))
