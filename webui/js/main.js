
function query() {
/*	var form = $('#search');
	var data = form.serialize();
	$.get('/api/search/', data, function(response) {
		alert(response);
	});*/

/*	var q = $("input:first").val();
	$.getJSON('/api/search/?q=' + q, function (json) {
		alert(json.result);
		$.each(json.list, function (i, fb) {
		alert(fb.result);
		});
	});*/

	var form = $('#search');
	var data = form.serialize();

	var results = $('#results');

	var q = $("input:first").val();
	$.getJSON('/api/search/?q=' + q, function (data) {
		//var items = [];
		results.empty()
		$.each(data, function(key, val) {
			if (key == 'results') {
				$.each(val, function(key, val) {
					results.append($('<tr>')
						.append($('<td>')
							.append($('<span>').text('icon'))
							.append($('<br/>'))
							.append($('<span>').text('['+val.category+']'))
						)
						.append($('<td>')
							.append($('<span>').text(val.filename))
							.append($('<br/>'))
							.append($('<span>', {'class': 'pull-left'}).text(val.size))
							.append($('<span>').text(val.filename))
							.append($('<span>', {'class': 'pull-right'}).text(val.mtime))
						)
					);
				});
			}

			//$('<td>', {'class': 'singleresult', html: key}).appendTo("#results");
			//items.push('<li id="' + key + '">' + val + '</li>');
		});

		//tableresults.append(items);

/*		$('<ul/>', {
			'class': 'my-new-list',
			html: items.join('')
		}).appendTo('body');*/
	});

	return false;
}
