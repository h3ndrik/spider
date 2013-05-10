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
        <form class="well form-search" id="search" action="javascript:query()">
          <fieldset>
            <div class="input-append span8">
              <input type="text" class="input-block-level search-query">
              <button type="submit" class="btn btn-primary">Search</button>
            </div>
          </fieldset>
        </form>
      </div>

%include div_results results=results

%include div_detail filedetail=filedetail

    </div> <!-- /container -->

%if results:
%    num_results=results['num_results'] or None
%    start=results['start'] or None
%    num=results['num'] or None
%else:
%    num_results = None
%    start = None
%    num = None
%end
%q = q or ''
%include pagination num_results=num_results, start=start, num=num, q=q

  </body>
