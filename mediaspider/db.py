from sqlalchemy.orm import sessionmaker
from mediaspider.models import *
from os import getpid
import logging

logger = logging.getLogger(__name__)

class DB(object):
    """Database interface"""
#    engine = None
#    session = None

    def __init__(self, database='sqlite:///spider.db'):
        engine = create_engine(database, convert_unicode=True, encoding='utf-8')
        #engine.raw_connection().connection.text_factory = str
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def getControl(self, name):
                return self.session.query(Control).filter(Control.name == name).one()

    def getJobs(self, name=None):
        if name:
            return [self.session.query(Control).\
                                    filter(Control.name == name).\
                                    filter(Control.crawl == 1).\
                                    one()]
        else:
            return self.session.query(Control).filter(Control.crawl == 1).all()

    def add(self, obj):
        self.session.add(obj)

    def delete(self, obj):
        self.session.delete(obj)

    def cleanTmpFiles(self):
        self.session.query(TmpFiles).delete()
        self.session.commit()

    def lock(self, item):
        item.pid_lock = getpid()
        self.session.commit()

    def unlock(self, item):
        item.pid_lock = 0
        self.session.commit()
