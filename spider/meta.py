import os
import re
import logging
from spider.meta_patterns import filetypes, pattern_strings
from spider.models import Metadata

logger = logging.getLogger(__name__)

class Meta(object):
    """Metadata handling for (multimedia-)files"""

    def __init__(self, db, name):
        self.db = db
        self.category = name

        # Compile regexs
        self.regexs = dict()
        for filetype in pattern_strings:
            self.regexs[filetype] = dict()
            for category in pattern_strings[filetype]:
                self.regexs[filetype][category] = dict()
                for patternname in pattern_strings[filetype][category]:
                    self.regexs[filetype][category][patternname] = []
                    for pattern in pattern_strings[filetype][category][patternname]:
                        try:
                            regex = re.compile(pattern, re.VERBOSE)
                        except (re.error, errormsg):
                            logger.warning("Invalid pattern (error: %s)\nPattern:\n%s" % (
                                errormsg, pattern))
                        else:
                            self.regexs[filetype][category][patternname].append(regex)
        self.regexs['other'] = dict()

    def insertmeta(self, filename, id):
        """gather metadata for 'filename' and write to metadata table"""
        if os.path.splitext(filename)[1].strip().lower() in filetypes['filetype_video']:
            filetype = 'video'
        elif os.path.splitext(filename)[1].strip().lower() in filetypes['filetype_audio']:
            filetype = 'audio'
        elif os.path.splitext(filename)[1].strip().lower() in filetypes['filetype_image']:
            filetype = 'image'
        elif os.path.splitext(filename)[1].strip().lower() in filetypes['filetype_text']:
            filetype = 'text'
        # Software
        # Games
        else:
            filetype = 'other'

        # TODO: Plugins

        # get cover.jpg
        cover = None
        try:
            if os.path.isdir(filename):
                path = filename
            else:
                path = os.path.dirname(filename)
            ppath = os.path.dirname(path)
            for look in [path, ppath]:
                if os.path.isfile(os.path.join(look,'cover.jpg')):
                    logger.info('Found cover.jpg')
                    cover = path+'/cover.jpg'
        except:
            pass

        match = None
        for category in self.regexs[filetype]:
            for patternname in self.regexs[filetype][category]:
                for regex in self.regexs[filetype][category][patternname]:
                    match = regex.match(filename)
                    if match:
                        keys = match.groupdict().keys()
                        item = Metadata(id=id, filetype=category, source=patternname, cover=cover, auto=True)
                        for key in keys:
                            if hasattr(item, key):
                                setattr(item, key, match.group(key))
                            else:
                                logger.info('Database has no column for %r' % key)
                        self.db.add(item)
                        #return  # Break on first match
        if not match:
            logger.info('No regex matched on %r' % filename)

