function go_home() {
	$('#div_search').show();
	$('#results').empty();
	$('#div_results').show();
	$('#btn_home').attr('class', 'active');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', '');
}

function go_search() {
	$('#div_search').show();
	$('#div_results').show();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', 'active');
	$('#btn_new').attr('class', '');
}

function go_new() {
	$('#div_search').hide();
	$('#div_results').show();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', 'active');
	get_new();
}

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

	var size = item.size;
	var mtime = item.mtime;
        var icon = "/mime/" + item.mime.substring(0, item.mime.indexOf("/")) + ".png";
	var category = '['+item.category+']';
	table.append($('<tr>')
		.append($('<td>')
			.append($('<span>')
				.append($('<a>', {href: link})
					.append($('<img/>', {src:'img'+icon}))
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
	$.getJSON('/api/search/?q=' + q, function (data) {
		//var items = [];
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

	return false;
}
