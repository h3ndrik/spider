      <div class="container" id="div_detail">

%try:
%if filedetail:
%    from spider.helper import size2human, timestamp2human
%    import os
%    detail = filedetail['detail']
%    if detail['mime']:
%        icon = '/img/mime/' + detail['mime'].split('/', 1)[0] + '.png'
%    else:
%        icon = '/img/mime/' + 'unknown' + '.png'
%    end
%    filename = os.path.basename(detail['link'])
%    path = os.path.dirname(detail['link'])
%    size = size2human(detail['size'])
%    age = timestamp2human(detail['mtime'])
%    try:
%        cover = filedetail['meta'][0]['coverlink']
%    except:
%        cover = None
%    end
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th><img src="{{icon}}" />&nbsp;{{filename}}</th>
            </tr>
          </thead>
          <tbody id="filedetail">
            <tr>
              <td>
%    if detail['mime'] and detail['mime'].startswith('video'):
                <video width="640" height="390" poster="{{cover if cover else ''}}" controls>
                  <source src="{{detail['link']}}" type="{{detail['mime']}}" />
                  This browser is not compatible with HTML5
                </video>
                <!-- test
<OBJECT classid="clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921" width="640" height="480" id="vlcviewerie">
<param name="MRL" value="{{detail['link']}}" />
<param name="ShowDisplay" value="False" />
<param name="AutoLoop" value="False" />
<param name="AutoPlay" value="True" />
<param name="Volume" value="100" />
<param name="toolbar" value="true" />
<embed type="application/x-vlc-plugin" src="{{detail['link']}}" pluginspage="http://www.videolan.org" version="VideoLAN.VLCPlugin.2" id="vlcviewer" autostart="1" loop="no" width="640" height="480" toolbar="true"></embed>
<noembed>VLC Plugin nicht gefunden..</noembed>
</OBJECT>
                 ende test -->

%    elif detail['mime'] and detail['mime'].startswith('audio'):
                <audio {{!'width="640" height="390" poster="'+cover+'"' if cover else ''}} controls>
                  <source src="{{detail['link']}}" type="{{detail['mime']}}" />
                  This browser is not compatible with HTML5
                </audio>
%    elif detail['mime'] and detail['mime'].startswith('image'):
                <img src="{{detail['link']}}" width="640" height="390"/>
%    elif detail['mime'] and detail['mime'].startswith('directory'):
                <ul>
                  <li><a href="/search/?q={{os.path.dirname(detail['filename'])}}">..</a></li>
%        for child in filedetail['children']:
%            childfilename = os.path.basename(child['filename'])
                  <li><a href="/detail/{{child['id']}}">{{childfilename}}</a></li>
%        end
                </ul>
%    end # if detail['mime']...
              </td>
            </tr>

            <tr>
              <td>
                <span><b>{{filename}}</b></span><br />
                <span class="pull-left">{{path}}</span><br />
%    if detail['removed']:
                <span>
                <span>THIS ITEM WAS REMOVED {{timestamp2human(detail['removed'])}}</span>
%    end
                <ul>
                  <li>MTime: {{age}}</li>
                  <li>Size: {{size}}</li>
                  <li><a href="{{detail['link']}}">Download</a></li>
                  <li>category=<b>{{detail['category']}}</b>, mimetype=<b>{{detail['mime']}}</b>, firstseen=<b>{{timestamp2human(detail['firstseen'])}}</b>, hash=<b>{{detail['hash']}}</b></li>
                </ul>
              </td>
            </tr>

%    for meta in filedetail['meta']:
            <tr>
              <td>
%#                <form class="" action="/api/updatemeta/">
%#                  <fieldset>
%#                    Series: <input type="text" class="" name="seriesname" value="{{meta['seriesname']}}">
%#                    <input type="text" class="" name="seasonnumber" size="4" maxlength="4" value="{{meta['seasonnumber']}}">
%#                    <input type="text" class="" name="episodenumber" size="4" maxlength="4" value="{{meta['episodenumber']}}">
%#                    Language: <input type="text" class="" name="language" value="{{meta['language'] or ''}}">
%#                      <button type="submit" class="btn btn-primary">Submit</button>
%#                  </fieldset>
%#                </form>
                <ul>
%        if meta['filetype'] == 'tv_show':
                  <li>Series: <b>{{meta['seriesname']}}</b></li>
                  <li>Season: {{meta['seasonnumber']}}, Episode: {{meta['episodenumber']}}</li>
%        elif meta['filetype'] == 'movie':
                  <li>Moviename: <b>{{meta['moviename']}}</b></li>
%        elif meta['filetype'] == 'album':
                  <li>Collection: {{meta['collection']}}</li>
                  <li>Artist: {{meta['artist']}}</li>
                  <li>{{meta['year']}} - {{meta['album']}}</li>
                  <li>{{meta['track']}} - {{meta['title']}}</li>
%        elif meta['filetype'] == 'ebook':
                  <li>Author: {{meta['author']}}</li>
%        end # if meta['filetype'] == ...

%        # Common Attributes:
                  <li>Language: {{meta['language']}}</li>
                </ul>
                <ul>
                  <li>Cover: <img src="{{meta['cover'] if meta['cover'] else ''}}" width="64" height="39" /></li>
                  <li>Duration: {{meta['duration']}}</li>
                  <li>Resolution: {{meta['resolution']}}</li>
                  <li>Codec: {{meta['codec']}}</li>
                  <li>Quality: {{meta['quality']}}</li>
                  <li>Group: {{meta['group']}}</li>
                  <li>Genre: {{meta['genre']}}</li>
                  <li>Tags: {{meta['tags']}}</li>
                  <li>Comment: {{meta['comment']}}</li>
                  <li>Auto: {{meta['auto']}}</li>
                  <li>Flag: {{meta['flag']}}</li>
                  <li>Source: {{meta['source']}}</li>
                </ul>
                <ul>
                  <li>Infos &uuml;bernehmen | Infos l&ouml;schen | Für den Admin markieren</li>
                </ul>
              </td>
            </tr>
%    end # for meta in filedetail['meta']:
          </tbody>
        </table>

        <script>$(document).ready(go_detail());</script>

%end # if filedetail
%except NameError:
%    pass
%end # try
      </div> <!-- id="div_detail" -->
