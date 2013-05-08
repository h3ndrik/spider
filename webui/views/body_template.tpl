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

          </tbody>
        </table>
      </div>

    </div> <!-- /container -->

%include pagination

    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/js/jquery.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>
    <script src="/js/main.js"></script>

  </body>
