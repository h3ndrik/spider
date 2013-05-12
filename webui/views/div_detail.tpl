      <div class="container" id="div_detail">

%try:
%if filedetail:
%    detail = filedetail['detail']
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>{{filedetail['detail']['filename']}}</th>
              <th>Detail</th>
            </tr>
          </thead>
          <tbody id="filedetail">
            <tr>
              <td>
%# Display 'cover.jpg' if exists
%    if detail['mime'].startswith('video'):
                <video width="640" height="390" controls>
                  <source src="/file/{{filedetail['detail']['filename']}}" type="{{filedetail['detail']['mime']}}" />
                  This browser is not compatible with HTML5
                </video>
                <!-- test
<OBJECT classid="clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921" width="640" height="480" id="vlcviewerie">
<param name="MRL" value="/file/{{filedetail['detail']['filename']}}" />
<param name="ShowDisplay" value="False" />
<param name="AutoLoop" value="False" />
<param name="AutoPlay" value="True" />
<param name="Volume" value="100" />
<param name="toolbar" value="true" />
<embed type="application/x-vlc-plugin" src="/file/{{filedetail['detail']['filename']}}" pluginspage="http://www.videolan.org" version="VideoLAN.VLCPlugin.2" id="vlcviewer" autostart="1" loop="no" width="640" height="480" toolbar="true"></embed>
<noembed>VLC Plugin nicht gefunden..</noembed>
</OBJECT>
                 ende test -->

%    elif detail['mime'].startswith('image'):
                <img src="{{filedetail['detail']['filename']}}" width="300" height="200"/>
%    end
              </td>
              <td>
%    from spider.helper import size2human, timestamp2human
%    for meta in filedetail['meta']:
                <ul>
%        if meta['filetype'] == 'tv_show':
                  <li>Series: {{meta['seriesname']}}</li>
                  <li>Season: {{meta['seasonnumber']}}</li>
                  <li>Episode: {{meta['episodenumber']}}</li>
%        end
%        if meta['filetype'] == 'album':
                  <li>Artist: {{meta['artist']}}</li>
                  <li>{{meta['year']}} - {{meta['album']}}</li>
                  <li>{{meta['track']}} - {{meta['title']}}</li>
                  <li>Genre: {{meta['genre']}}</li>
                  <li>Collection: {{meta['collection']}}</li>
%        end
                  <li>Duration: {{meta['duration']}}</li>
                  <li>Language: {{meta['language']}}</li>
                  <li>Resolution: {{meta['resolution']}}</li>
                  <li>Codec: {{meta['codec']}}</li>
                  <li>Quality: {{meta['quality']}}</li>
                  <li>Group: {{meta['group']}}</li>

                  <li>Tags: {{meta['tags']}}</li>
                  <li>Comment: {{meta['comment']}}</li>
                  <li>Auto: {{meta['auto']}}</li>
                  <li>Flag: {{meta['flag']}}</li>
                  <li>Source: {{meta['source']}}</li>
                </ul>
%    end
              </td>
            </tr>
            <tr>
              <td>
                <ul>
                  <span><b>{{filedetail['detail']['filename']}}</b></span>
                  <li>Category: {{filedetail['detail']['category']}}</li>
                  <li>MTime: {{timestamp2human(filedetail['detail']['mtime'])}}</li>
                  <li>Firstseen: {{timestamp2human(filedetail['detail']['firstseen'])}}</li>
                  <li>Size: {{size2human(filedetail['detail']['size'])}}</li>
                  <li>Mimetype: {{filedetail['detail']['mime']}}</li>
                  <li>Hash: {{filedetail['detail']['hash']}}</li>
                  <li>Removed: {{filedetail['detail']['removed']}}</li>
                </ul>
              </td>
              <td></td>
            </tr>
          </tbody>
        </table>

        <script>$(document).ready(go_detail());</script>

%end
%except NameError:
%    pass
%end
      </div> <!-- id="div_detail" -->
