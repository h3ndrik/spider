<!DOCTYPE html>
<html lang="en">
%include header_template title=title
  <body>
%include navbar title=title

    <div class="container">

      <div class="container" id="div_detail">

        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>{{rows['detail']['filename']}}</th>
              <th>Detail</th>
            </tr>
          </thead>
          <tbody id="results">
            <tr>
              <td><img src="" width="300" height="200"/></td>
              <td>
% from spider.helper import size2human, timestamp2human
% for meta in rows['meta']:
                <ul>
%     if meta['filetype'] == 'tv_show':
                  <li>Series: {{meta['seriesname']}}</li>
                  <li>Season: {{meta['seasonnumber']}}</li>
                  <li>Episode: {{meta['episodenumber']}}</li>
%     end
%     if meta['filetype'] == 'album':
                  <li>Artist: {{meta['artist']}}</li>
                  <li>{{meta['year']}} - {{meta['album']}}</li>
                  <li>{{meta['track']}} - {{meta['title']}}</li>
                  <li>Genre: {{meta['genre']}}</li>
                  <li>Collection: {{meta['collection']}}</li>
%     end
                  <li>Duration: {{meta['duration']}}</li>
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
% end
              </td>
            </tr>
            <tr>
              <td>
                <ul>
                  <span><b>{{rows['detail']['filename']}}</b></span>
                  <li>Category: {{rows['detail']['category']}}</li>
                  <li>MTime: {{timestamp2human(rows['detail']['mtime'])}}</li>
                  <li>Firstseen: {{timestamp2human(rows['detail']['firstseen'])}}</li>
                  <li>Size: {{size2human(rows['detail']['size'])}}</li>
                  <li>Mimetype: {{rows['detail']['mime']}}</li>
                  <li>Hash: {{rows['detail']['hash']}}</li>
                  <li>Removed: {{rows['detail']['removed']}}</li>
                </ul>
              </td>
              <td></td>
            </tr>
          </tbody>
        </table>


      </div>

    </div> <!-- /container -->

    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/js/jquery.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>
    <script src="/js/main.js"></script>

  </body>


</html>

