#!/usr/bin/env python

filetypes = {'filetype_video':[".m4v", ".3gp", ".nsv", ".ts", ".ty", ".strm", ".rm", ".rmvb", ".m3u", ".ifo", ".mov", ".qt", ".divx", ".xvid", ".bivx", ".vob", ".nrg", ".img", ".iso", ".pva", ".wmv", ".asf", ".asx", ".ogm", ".m2v", ".avi", ".bin", ".dat", ".dvr-ms", ".mpg", ".mpeg", ".mp4", ".mkv", ".avc", ".vp3", ".svq3", ".nuv", ".viv", ".dv", ".fli", ".flv", ".rar", ".001", ".wpl", ".zip"],

    'filetype_audio':[".nsv", ".m4a", ".flac", ".aac", ".strm", ".pls", ".rm", ".mpa", ".wav", ".wma", ".ogg", ".mp3", ".mp2", ".m3u", ".mod", ".amf", ".669", ".dmf", ".dsm", ".far", ".gdm", ".imf", ".it", ".m15", ".med", ".okt", ".s3m", ".stm", ".sfx", ".ult", ".uni", ".xm", ".sid", ".ac3", ".dts", ".cue", ".aif", ".aiff", ".wpl", ".ape", ".mac", ".mpc", ".mp+", ".mpp", ".shn", ".zip", ".rar", ".wv", ".nsf", ".spc", ".gym", ".adplug", ".adx", ".dsp", ".adp", ".ymf", ".ast", ".afc", ".hps", ".xsp"],

    'filetype_image':[".png", ".jpg", ".jpeg", ".bmp", ".gif", ".ico", ".tif", ".tiff", ".tga", ".pcx", ".cbz", ".zip", ".cbr", ".rar", ".m3u"],

    'filetype_text':[".txt", ".pdf", ".lit", ".doc", ".html", ".htm", ".epub", ".zip", ".rar", ".tar", ".gz", ".bz2", ".7z"],
}

pattern_strings = {
    'video': {
    'tv_show': {
    # Patterns to parse tv_shows input filenames with ((c)tvnamer)
    'filename_patterns_tv_shows': [
        # [group] Show - 01-02 [crc]
        '''^(.*\\/)*
        \[(?P<group>.+?)\][ ]?               # group name, captured for [#100]
        (?P<seriesname>.*?)[ ]?[-_][ ]?          # show name, padding, spaces?
        (?P<episodenumberstart>\d+)              # first episode number
        ([-_]\d+)*                               # optional repeating episodes
        [-_](?P<episodenumberend>\d+)            # last episode number
        (?=                                      # Optional group for crc value (non-capturing)
          .*                                     # padding
          \[(?P<crc>.+?)\]                       # CRC value
        )?                                       # End optional crc group
        [^\/]*$''',

        # [group] Show - 01 [crc]
        '''^(.*\\/)*
        \[(?P<group>.+?)\][ ]?               # group name, captured for [#100]
        (?P<seriesname>.*)                       # show name
        [ ]?[-_][ ]?                             # padding and seperator
        (?P<episodenumber>\d+)                   # episode number
        (?=                                      # Optional group for crc value (non-capturing)
          .*                                     # padding
          \[(?P<crc>.+?)\]                       # CRC value
        )?                                       # End optional crc group
        [^\/]*$''',

        # foo s01e23 s01e24 s01e25 *
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        ([\.\- ]+                                # separator
        [Ss](?P=seasonnumber)                    # s01
        [\.\- ]?                                 # separator
        [Ee][0-9]+)*                             # e24 etc (middle groups)
        ([\.\- ]+                                # separator
        [Ss](?P=seasonnumber)                    # last s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberend>[0-9]+))        # final episode number
        [^\/]*$''',

        # foo.s01e23e24*
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        ([\.\- ]?                                # separator
        [Ee][0-9]+)*                             # e24e25 etc
        [\.\- ]?[Ee](?P<episodenumberend>[0-9]+) # final episode num
        [^\/]*$''',

        # foo.1x23 1x24 1x25
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # first season number (1)
        [xX](?P<episodenumberstart>[0-9]+)       # first episode (x23)
        ([ \._\-]+                               # separator
        (?P=seasonnumber)                        # more season numbers (1)
        [xX][0-9]+)*                             # more episode numbers (x24)
        ([ \._\-]+                               # separator
        (?P=seasonnumber)                        # last season number (1)
        [xX](?P<episodenumberend>[0-9]+))        # last episode number (x25)
        [^\/]*$''',

        # foo.1x23x24*
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # 1
        [xX](?P<episodenumberstart>[0-9]+)       # first x23
        ([xX][0-9]+)*                            # x24x25 etc
        [xX](?P<episodenumberend>[0-9]+)         # final episode num
        [^\/]*$''',

        # foo.s01e23-24*
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        (                                        # -24 etc
             [\-]
             [Ee]?[0-9]+
        )*
             [\-]                                # separator
             [Ee]?(?P<episodenumberend>[0-9]+)   # final episode num
        [\.\- ]                                  # must have a separator (prevents s01e01-720p from being 720 episodes)
        [^\/]*$''',

        # foo.1x23-24*
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # 1
        [xX](?P<episodenumberstart>[0-9]+)       # first x23
        (                                        # -24 etc
             [\-+][0-9]+
        )*
             [\-+]                               # separator
             (?P<episodenumberend>[0-9]+)        # final episode num
        ([\.\-+ ].*                              # must have a separator (prevents 1x01-720p from being 720 episodes)
        |
        $)''',

        # foo.[1x09-11]*
        '''^(.*\\/)*
        (?P<seriesname>.+?)[ \._\-]          # show name and padding
        \[                                       # [
            ?(?P<seasonnumber>[0-9]+)            # season
        [xX]                                     # x
            (?P<episodenumberstart>[0-9]+)       # episode
            ([\-+] [0-9]+)*
        [\-+]                                    # -
            (?P<episodenumberend>[0-9]+)         # episode
        \]                                       # \]
        [^\\/]*$''',

        # foo - [012]
        '''^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?       # show name and padding
        \[                                       # [ not optional (or too ambigious)
        (?P<episodenumber>[0-9]+)                # episode
        \]                                       # ]
        [^\\/]*$''',
        # foo.s0101, foo.0201
        '''^
        (?P<seriesname>.+?)[ \._\-]
        [Ss](?P<seasonnumber>[0-9]{2})
        [\.\- ]?
        (?P<episodenumber>[0-9]{2})
        [^0-9]*$''',

        # foo.1x09*
        '''^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?       # show name and padding
        \[?                                      # [ optional
        (?P<seasonnumber>[0-9]+)                 # season
        [xX]                                     # x
        (?P<episodenumber>[0-9]+)                # episode
        \]?                                      # ] optional
        [^\\/]*$''',

        # foo.s01.e01, foo.s01_e01, "foo.s01 - e01"
        '''^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?
        \[?
        [Ss](?P<seasonnumber>[0-9]+)[ ]?[\._\- ]?[ ]?
        [Ee]?(?P<episodenumber>[0-9]+)
        \]?
        [^\\/]*$''',

        # foo.2010.01.02.etc
        '''
        ^(.*\\/)*
        ((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<year>\d{4})                          # year
        [ \._\-]                                 # separator
        (?P<month>\d{2})                         # month
        [ \._\-]                                 # separator
        (?P<day>\d{2})                           # day
        [^\/]*$''',

        # foo - [01.09]
        '''^(.*\\/)*
        ((?P<seriesname>.+?))                # show name
        [ \._\-]?                                # padding
        \[                                       # [
        (?P<seasonnumber>[0-9]+?)                # season
        [.]                                      # .
        (?P<episodenumber>[0-9]+?)               # episode
        \]                                       # ]
        [ \._\-]?                                # padding
        [^\\/]*$''',

        # Foo - S2 E 02 - etc
        '''^(.*\\/)*
        (?P<seriesname>.+?)[ ]?[ \._\-][ ]?
        [Ss](?P<seasonnumber>[0-9]+)[\.\- ]?
        [Ee]?[ ]?(?P<episodenumber>[0-9]+)
        [^\\/]*$''',

        # Show - Episode 9999 [S 12 - Ep 131] - etc
        '''^(.*\\/)*
        (?P<seriesname>.+)                       # Showname
        [ ]-[ ]                                  # -
        [Ee]pisode[ ]\d+                         # Episode 1234 (ignored)
        [ ]
        \[                                       # [
        [sS][ ]?(?P<seasonnumber>\d+)            # s 12
        ([ ]|[ ]-[ ]|-)                          # space, or -
        ([eE]|[eE]p)[ ]?(?P<episodenumber>\d+)   # e or ep 12
        \]                                       # ]
        .*$                                      # rest of file
        ''',

        # show name 2 of 6 - blah
        '''^(.*\\/)*
        (?P<seriesname>.+?)                  # Show name
        [ \._\-]                                 # Padding
        (?P<episodenumber>[0-9]+)                # 2
        of                                       # of
        [ \._\-]?                                # Padding
        \d+                                      # 6
        ([\._ -]|$|[^\\/]*$)                     # More padding, then anything
        ''',

        # Show.Name.Part.1.and.Part.2
        '''^(.*\\/)*
        (?i)
        (?P<seriesname>.+?)                        # Show name
        [ \._\-]                                   # Padding
        (?:part|pt)?[\._ -]
        (?P<episodenumberstart>[0-9]+)             # Part 1
        (?:
          [ \._-](?:and|&|to)                        # and
          [ \._-](?:part|pt)?                        # Part 2
          [ \._-](?:[0-9]+))*                        # (middle group, optional, repeating)
        [ \._-](?:and|&|to)                        # and
        [ \._-]?(?:part|pt)?                       # Part 3
        [ \._-](?P<episodenumberend>[0-9]+)        # last episode number, save it
        [\._ -][^\\/]*$                            # More padding, then anything
        ''',

        # Show.Name.Part1
        '''^(.*\\/)*
        (?P<seriesname>.+?)                  # Show name\n
        [ \\._\\-]                               # Padding\n
        [Pp]art[ ](?P<episodenumber>[0-9]+)      # Part 1\n
        [\\._ -][^\\/]*$                         # More padding, then anything\n
        ''',

        # show name Season 01 Episode 20
        '''^(.*\\/)*
        (?P<seriesname>.+?)[ ]?               # Show name
        [Ss]eason[ ]?(?P<seasonnumber>[0-9]+)[ ]? # Season 1
        [Ee]pisode[ ]?(?P<episodenumber>[0-9]+)   # Episode 20
        [^\\/]*$''',                              # Anything

        # foo.103*
        '''^(.*\\/)*
        (?P<seriesname>.+)[ \._\-]
        (?P<seasonnumber>[0-9]{1})
        (?P<episodenumber>[0-9]{2})
        [\._ -][^\\/]*$''',

        # foo.0103*
        '''^(.*\\/)*
        (?P<seriesname>.+)[ \._\-]
        (?P<seasonnumber>[0-9]{2})
        (?P<episodenumber>[0-9]{2,3})
        [\._ -][^\\/]*$''',

        # show.name.e123.abc
        '''^(.*\\/)*
        (?P<seriesname>.+?)                  # Show name
        [ \._\-]                                 # Padding
        [Ee](?P<episodenumber>[0-9]+)            # E123
        [\._ -][^\\/]*$                          # More padding, then anything
        ''',
    ],

    # Own patterns (c) h3ndrik (wtftpl)
    'path_patterns_tv_shows': [
        # /path/TV Shows/MythBusters/Season 01 [D, E]/MythBusters 01x05 A great eposide.avi
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([tT][vV]([ \._\-][sS]how[s]?)?|([tT][vV][ \._\-])?[sS]erie[n]?) # TV Shows directory
        [\/]                                    # new directory
        (?P<seriesname>[^\/]+)                  # Showname
        [\/]                                    # new directory
        (
        ([sS]taffel|[sS]eries|[sS]eason)?[ \._\-]?  # Season
        (?P<seasonnumber>[0-9]+)                # seasonnumber
        ([ ,\._\-]+[\[(](?P<language>[^\/]+?)[\])])?  # language, optional
        [\/]                                    # new directory
        )?                                      # season directory is optional
        [^\/]*?                                 # anything (non-greedy) (probably seasonname(again))
        (
        [0-9]*                                  # season (again,ignored), to not ignore: (?P=seasonnumber)+
        [^\/0-9]+                               # something
        )?                                      # season(again) is optional
        (?P<episodenumber>\d+)                  # episode
        [ \._\-][^\/]*$                         # padding, then anything
        ''',
    ],
    },
    'movie': {
    'path_patterns_movies': [
        # /path/Movies/Star Trek IV/HD, [D, E]/Star Trek IV - Best movie ever.avi
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([mM]ovie[s]?|[fF]ilm[e]?)              # Movies directory
        [\/]                                    # new directory
        (
        (?P<collection>[^\/]+?)                 # Collection, non-greedy
        [\/]                                    # new directory
        )??                                     # collection is optional, and non-greedy (or should quality be non-greedy?)
        (?P<moviename>[^\/]+)                   # Moviename
        [\/]                                    # new directory
        (
        (?P<quality>[^\/]+?)                    # quality
        ([ ,\._\-]+[\[(](?P<language>[^\/]+?)[\])])?  # language, optional
        [\/]                                    # new directory
        )?                                      # quality is optional
        [^\/]*$                                 # filename (ignored)
        ''',

        # /path/Movies/Star Trek IV (E).avi
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([mM]ovie[s]?|[fF]ilm[e]?)              # Movies directory
        [\/]                                    # new directory
        (?P<moviename>[^\/]+)                   # Moviename
        ([ ,\._\-]+[\[(](?P<language>[^\/]+?)[\])])?  # language, optional
        \.                                      # dot
        [^\/]*$                                 # fileextension
        ''',
    ],
    },
    },
    'audio': {
    'album': {
    'path_patterns_albums': [
        # /path/Alben/Artist/Album/01 - Title.mp3
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([aA]lben)                              # Alben directory
        [\/]                                    # new directory
        (?P<artist>[^\/]+)                      # Artist
        [\/]                                    # new directory
        ((?P=artist)+[ \._\-]+)?                # optional artist+whitespace again
        (?P<album>[^\/]+)                       # Album
        [\/]                                    # new directory
        ((?P=artist)+[ \._\-]+)?                # optional artist+whitespace again
        (
        (?P<track>\d+)                          # track
        [ \._\-]*                               # whitespace
        )?                                      # track is optional
        (?P<title>[^\/]+)                       # Title
        \.                                      # dot
        [^\/]*$                                 # fileextension
        ''',
    ],
    },
    'sampler': {
    'path_patterns_sampler': [
        # /path/Sampler/Collection/01 - Title.mp3
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([sS]ampler|[sS]oundtrack[s]?)          # Sampler directory
        [\/]                                    # new directory
        (?P<collection>[^\/]+)                  # Sampler name
        [\/]                                    # new directory
        (
        (?P<track>\d+)                          # track
        [ \._\-]*                               # whitespace
        )?                                      # track is optional
        (?P<artist>[^\/]+)                      # artist
        [ \._\-]+                               # whitespace
        (?P<title>[^\/]+)                       # Title
        \.                                      # dot
        [^\/]*$                                 # fileextension
        ''',
    ],
    },
    'audiobook': {
    'path_patterns_audiobooks': [
        # /path/Audiobooks/Artist/Collection/Album/01 - Track.mp3
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([aA]udiobook[s]?)                      # Audiobooks directory
        [\/]                                    # new directory
        (
        (?P<artist>[^\/]+?)                     # Artist, non-greedy
        [\/]                                    # new directory
        )?                                      # Artist is optional
        (?P<collection>[^\/]+)                  # Collection
        [\/]                                    # new directory
        (
        (?P<album>[^\/]+)                       # Album
        [\/]                                    # new directory
        )?                                      # Album is optional
        (?P<track>\d+)?                         # track (optional)
        [ \._\-]*                               # whitespace
        (?P<title>[^\/]+)                       # Title
        \.                                      # dot
        [^\/]*$                                 # fileextension
        ''',
    ],
    },
    },
    'text': {
    'ebook': {
    'path_patterns_ebooks': [
        # /path/E-Books/Browne, Dik/Hägar der Schreckliche/Eheglück.pdf
        '''^.*                                  # path prefix
        [\/]                                    # new directory
        ([eE][ \._\-]?[bB]ook[s]?)              # E-Books directory
        [\/]                                    # new directory
        (?P<author>[^\/]+)                      # Author
        [\/]                                    # new directory
        (?P<collection>[^\/]+)                  # Collection
        [\/]                                    # new directory
        (?P<title>[^\/]+)                       # Title
        \.                                      # dot
        [^\/]*$                                 # fileextension
        ''',
    ],
    },
    },
    'executable': {
    'game': {
    'path_patterns_games': [
    ],
    },
    'software': {
    'path_patterns_software': [
    ],
    },
    },
    'image': {
    'image': {
    'path_patterns_images': [
    ],
    },
    },
}
