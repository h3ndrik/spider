import os
import re
import logging
from spider.meta_strings import strings
from spider.models import Metadata

class Meta(object):

    def __init__(self, db, name):
        self.db = db
        self.category = name
        self.tv_regexs = []

        for pattern in strings['filename_patterns_tv_shows']:
            try:
                regex = re.compile(pattern, re.VERBOSE)
            except (re.error, errormsg):
                logging.warning("Invalid episode_pattern (error: %s)\nPattern:\n%s" % (
                    errormsg, pattern))
            else:
                self.tv_regexs.append(regex)

    def insertmeta(self, filename, id):
        if os.path.splitext(filename)[1].strip().lower() in strings['filetype_video']:
            filetype = 'video'
            for regex in self.tv_regexs:
                match = regex.match(os.path.basename(filename))
                if match:
                    seriesname = None
                    seasonnumber = None
                    episodenumber = None
                    group = None
                    keys = match.groupdict().keys()
                    if 'seriesname' in keys:
                        seriesname = match.group('seriesname')
                    if 'seasonnumber' in keys:
                        seasonnumber = match.group('seasonnumber')
                    if 'episodenumber' in keys:
                        episodenumber = match.group('episodenumber')
                    if 'group' in keys:
                        group = match.group('group')
                    if 'episodenumberstart' in keys:
                        episodenumber = ''.join([match.group('episodenumberstart'), '-', match.group('episodenumberend')])
                    if 'year' in keys:
                        episodenumber = ''.join([episodenumber, match.group('year')])
                    if 'month' in keys:
                        episodenumber = ''.join([episodenumber, '-', match.group('month')])
                    if 'day' in keys:
                        episodenumber = ''.join([episodenumber, '-', match.group('year')])
                    item = Metadata(id=id, filetype=filetype, seriesname=seriesname, seasonnumber=seasonnumber, episodenumber=episodenumber, group=group)
                    self.db.add(item)
                    return
            logging.info('Cannot parse %r' % filename)

        elif os.path.splitext(filename)[1].strip().lower() in strings['filetype_audio']:
            filetype = 'audio'
        elif os.path.splitext(filename)[1].strip().lower() in strings['filetype_picture']:
            filetype = 'picture'
        # E-Book
        # Software
        else:
            filetype = 'other'
