function go_home() {
	$('#div_search').show();
	$('#results').empty();
	$('#div_results').hide();
	$('#div_detail').hide();
	$('#btn_home').attr('class', 'active');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', '');
}

function go_search() {
	$('#div_search').show();
//	$('#div_results').show();
	$('#div_detail').hide();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', 'active');
	$('#btn_new').attr('class', '');
//	query();
}

function go_new() {
	$('#div_search').hide();
//	$('#div_results').show();
	$('#div_detail').hide();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', 'active');
//	get_new();
}

function go_detail() {
	$('#div_search').hide();
	$('#div_results').hide();
	$('#div_detail').show();
	$('#btn_home').attr('class', '');
	$('#btn_search').attr('class', '');
	$('#btn_new').attr('class', '');
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
