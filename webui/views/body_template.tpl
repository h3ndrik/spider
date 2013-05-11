%if results:
%    num_results=results['num_results'] or None
%    start=results['start'] or 0
%    num=results['num'] or 20
%else:
%    num_results = None
%    start = start or 0
%    num = num or 20
%end
%q = q or ''

  <body>
%include navbar title=title

    <div class="container">

      <div class="container" id="div_logo">
        <!--<a href="/"><img src="img/logo.png" width="572" height="210"/></a>-->
        <h1 class="text-center">Suche</h1>
      </div>

      <div class="container text-center" id="div_message">
        <p>Beta</p>
      </div>

      <div class="container" id="div_search">
        <form class="well form-search" id="search" action="/suche/">
          <fieldset>
            <div class="input-append span8">
              <input type="text" class="input-block-level search-query" name="q" value="{{q}}">
              <!--<input name="start" type=hidden value="{{start}}">-->
              <!--<input name="num" type=hidden value="{{num}}">-->
              <button type="submit" class="btn btn-primary">Search</button>
            </div>
          </fieldset>
        </form>
      </div>

%include div_results results=results

%include div_detail filedetail=filedetail

    </div> <!-- /container -->

%include pagination num_results=num_results, start=start, num=num, q=q

  </body>
