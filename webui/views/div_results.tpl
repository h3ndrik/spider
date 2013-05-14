      <div class="container" id="div_results">
        <h2>Ergebnisse</h2>
        <!-- Tabelle mit abwechselnder Zellenhintergrundfarbe und Außenrahmen -->
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>Icon</th>
              <th>Filename</th>
            </tr>
          </thead>
          <tbody id="results">

%try:
%    if results:
%    from spider.helper import size2human, timestamp2human
%    import os.path
%        for result in results['results']:
%            if result['mime']:
%                icon = '/img/mime/' + result['mime'].split('/', 1)[0] + '.png'
%            else:
%                icon = '/img/mime/' + 'unknown' + '.png'
%            end
%            filename = os.path.basename(result['link'])
%            path = os.path.dirname(result['link'])
%            size = size2human(result['size'])
%            age = timestamp2human(result['mtime'])
            <tr>
              <td>
                <span>
                  <a href="/detail/{{result['id']}}">
                    <img src="{{icon}}" />
                  </a>
                </span><br />
                <span>[{{result['category']}}]</span>
              </td>
              <td>
                <span>
                  <a href="/detail/{{result['id']}}">{{filename}}</a>
                </span><br />
                <span class="pull-left span1">{{size}}</span>
                <span>{{path}}</span>
                <span class="pull-right">{{age}}</span>
              </td>
            </tr>
%        end

%    end
%except NameError:
%    pass
%end

          </tbody>
        </table>
      </div>
