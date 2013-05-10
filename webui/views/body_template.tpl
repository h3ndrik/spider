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

%include div_results

%include div_detail filedetail=filedetail

    </div> <!-- /container -->

%include pagination

  </body>
