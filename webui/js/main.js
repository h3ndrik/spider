function go_home() {
	$('#div_search').show();
	$('#results').empty();
	$('#div_results').hide();
	$('#btn_home').attr('class', 'active');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', '');
}

function go_search() {
	$('#div_search').show();
//	$('#div_results').show();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', 'active');
	$('#btn_new').attr('class', '');
	query();
}

function go_new() {
	$('#div_search').hide();
//	$('#div_results').show();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', 'active');
	get_new();
}

function size2human(size) {
    var units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    var i = 0;
    while(size >= 1024 || size <= -1024) {
        size /= 1024;
        ++i;
    }
    return size.toFixed(1) + ' ' + units[i];
}

function timestamp2human (timestamp) {

    function numberEnding (number) { //todo: replace with a wiser code
        return (number > 1) ? 's' : '';
    }

    var current_time_milliseconds = new Date().getTime();
    var current_time = current_time_milliseconds / 1000;
    var temp = current_time - timestamp;
    var suffix = " ago";
    if (temp < 0) {
        var suffix = " ahead";
        temp = 0 - temp;
    }

    var years = Math.floor(temp / 31536000);
    if (years) {
        return years + ' year' + numberEnding(years) + suffix;
    }
    var days = Math.floor((temp %= 31536000) / 86400);
    if (days) {
        return days + ' day' + numberEnding(days) + suffix;
    }
    var hours = Math.floor((temp %= 86400) / 3600);
    if (hours) {
        return hours + ' hour' + numberEnding(hours) + suffix;
    }
    var minutes = Math.floor((temp %= 3600) / 60);
    if (minutes) {
        return minutes + ' minute' + numberEnding(minutes) + suffix;
    }
    var seconds = temp % 60;
    if (seconds) {
        return seconds + ' second' + numberEnding(seconds) + suffix;
    }
    return 'just now'; //'less then a second' //or other string you like;
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

	var size = size2human(item.size);
	var mtime = timestamp2human(item.mtime);
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
