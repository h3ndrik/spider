import os
import re
import logging
from spider.meta_strings import strings
from spider.models import Metadata

class Meta(object):
    """Metadata handling for (multimedia-)files"""

    def __init__(self, db, name):
        self.db = db
        self.category = name
        self.video_regexs = []
        self.audio_regexs = []
        self.image_regexs = []

        for pattern in strings['filename_patterns_tv_shows'] + strings['path_patterns_tv_shows']:
            try:
                regex = re.compile(pattern, re.VERBOSE)
            except (re.error, errormsg):
                logging.warning("Invalid pattern (error: %s)\nPattern:\n%s" % (
                    errormsg, pattern))
            else:
                self.video_regexs.append(regex)

    def insertmeta(self, filename, id):
        """gather metadata for 'filename' and write to metadata table"""
        if os.path.splitext(filename)[1].strip().lower() in strings['filetype_video']:
            filetype = 'video'
            regexs = self.video_regexs
        elif os.path.splitext(filename)[1].strip().lower() in strings['filetype_audio']:
            filetype = 'audio'
            regexs = self.audio_regexs
            #TODO
        elif os.path.splitext(filename)[1].strip().lower() in strings['filetype_image']:
            filetype = 'image'
            regexs = self.image_regexs
            #TODO
        # E-Book
        # Software
        else:
            filetype = 'other'
            regexs = []

        for regex in regexs:
            match = regex.match(filename)
            if match:
                source = None # TODO
                keys = match.groupdict().keys()
                item = Metadata(id=id)
                for key in keys:
                    if hasattr(item, key):
                        item[key] = match.group(key)
                    else:
                        logging.info('Database has no column for %r' % key)
                self.db.add(item)
                return   # break on first match
        if not match:
            logging.info('No regex matched on %r' % filename)

