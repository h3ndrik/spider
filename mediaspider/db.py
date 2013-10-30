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
        self.connect(database)

    def connect(self, database='sqlite:///spider.db'):
        """Connect to Database at 'database'"""
        engine = create_engine(database, convert_unicode=True, encoding='utf-8')
        #engine.raw_connection().connection.text_factory = str
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def close(self, database='sqlite:///spider.db'):
        self.commit()
        self.session.close()  # remove()?
        #engine?

    def commit(self):
        """Issue a commit command to the Database"""
        self.session.commit()

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
        """Add a document to the database"""

#    def add_many(self, docs)
#        """Add several documents to the database"""
        self.session.add(obj)

    def delete(self, obj):
        self.session.delete(obj)

#    def delete_many(self, ids)
#        """Delete documents using an iterable of ids"""
#    def delete_query(self, query)
#        """Delete all documents identified by a query"""




    def cleanTmpFiles(self):
        self.session.query(TmpFiles).delete()
        self.session.commit()

    def lock(self, item):
        item.pid_lock = getpid()
        self.session.commit()

    def unlock(self, item):
        item.pid_lock = 0
        self.session.commit()
