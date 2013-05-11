function append_result(item, table) {
	var link = '/detail/'+item.id;
	var path = item.filename.substring(0, item.filename.lastIndexOf("/"));
	var filename = item.filename.substring(item.filename.lastIndexOf("/"));
        if (!item.mime || 0 === item.mime.length) {
		item.mime = "unknown";
	}
	if (item.mime.indexOf("/") == -1) {
		item.mime += "/";
	}

	var size = size2human(item.size);
	var mtime = timestamp2human(item.mtime);
        var icon = "/mime/" + item.mime.substring(0, item.mime.indexOf("/")) + ".png";
	var category = '['+item.category+']';
	table.append($('<tr>')
		.append($('<td>')
			.append($('<span>')
				.append($('<a>', {href: link})
					.append($('<img/>', {src:'/img'+icon}))
				)
			)
			.append($('<br/>'))
			.append($('<span>').text(category))
		)
		.append($('<td>')
			.append($('<span>')
				.append($('<a>', {href:link, text:filename}))
			)
			.append($('<br/>'))
			.append($('<span>', {'class': 'pull-left span1'}).text(size))
			.append($('<span>').text(path))
			.append($('<span>', {'class': 'pull-right'}).text(mtime))
		)
	);
}

function get_new() {
	var table = $('#results');
	$.getJSON('/api/new/', function (data) {
		table.empty()
		$('#div_results').show();
		$.each(data, function(key, val) {
			if (key == 'results') {
				$.each(val, function(key, val) {
					append_result(val, table);
				});
			}
		});
	});
}

function query() {
	var form = $('#search');
	var data = form.serialize();

	var table = $('#results');

	var q = $("input:first").val();

	if (!q || 0 === q.length) {
		table.empty();
		$('#div_results').show();
		return false;
	}

	$.getJSON('/api/search/?q=' + q, function (data) {
		table.empty();
		$('#div_results').show();
		$.each(data, function(key, val) {
			if (key == 'results') {
				$.each(val, function(key, val) {
					append_result(val, table);

				});
			}

		});

	});

	return false;
}
