  <body>
%include navbar title=title

    <div class="container">

      <h1>Suche</h1>
      <p>Beispiel für ein einfaches Suchformular.</p>

      <!-- Suchformular mit Eingabefeld und Button -->
      <form class="well form-search" action="/suche" method="get">
        <fieldset>
          <div class="input-append">
            <input type="text" class="input-block-level search-query">
            <button type="submit" class="btn btn-primary">Search</button>
          </div>
        </fieldset>
      </form>
 
      <h2>Ergebnisse</h2>
 
      <!-- Tabelle mit abwechselnder Zellenhintergrundfarbe und Außenrahmen -->
      <table class="table table-striped table-bordered ">
        <thead>
          <tr>
            <th>#</th>
            <th>Title</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Lorem ipsum dolor sit amet</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Consetetur sadipscing elitr</td>
          </tr>
          <tr>
            <td>3</td>
            <td>At vero eos et accusam</td>
          </tr>
        </tbody>
      </table>
    </div> <!-- /container -->

%include pagination

    <!-- Placed at the end of the document so the pages load faster -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>

  </body>
