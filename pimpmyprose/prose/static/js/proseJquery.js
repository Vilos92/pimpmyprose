// Function from django documentation to get csrf token for POST requests
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// jQuery functions for voting
$('.upvote').click( function() {
	var csrftoken = getCookie( 'csrftoken' );

	var pimp_id;
	pimp_id = $(this).attr("data-pimp_id");

	$.post('/upvote/', { csrfmiddlewaretoken : csrftoken, pimp_id : pimp_id }, function( data ) {
		var scoreID = '#pimp_' + pimp_id + '_score';

		// Data returned from get query is the new score for this pimp
		$( scoreID ).html( data );
	} );
} );

$('.downvote').click( function() {
	var csrftoken = getCookie( 'csrftoken' );

	var pimp_id;
	pimp_id = $(this).attr("data-pimp_id");

	$.post('/downvote/', { csrfmiddlewaretoken : csrftoken, pimp_id : pimp_id }, function( data ) {
		var scoreID = '#pimp_' + pimp_id + '_score';

		// Data returned from get query is the new score for this pimp
		$( scoreID ).html( data );
	} );
} );

// jQuery functions for following and unfollowing
$('.followButton').click( function() {
	var csrftoken = getCookie( 'csrftoken' );

	var user_id;
	user_id = $(this).attr("data-user_id");
	$.post('/follow/', { csrfmiddlewaretoken : csrftoken, user_id : user_id }, function( data ) {
		var followClass = '.user_' + user_id + '_follow';

		$( followClass ).html( data );
	} );
} );
