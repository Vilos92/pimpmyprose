// jQuery functions for voting
$('.upvote').click( function() {
	var pimp_id;
	pimp_id = $(this).attr("data-pimp_id");
	$.get('/upvote/', { pimp_id : pimp_id }, function(data) {
		var scoreID = '#pimp_' + pimp_id + '_score';
		console.log(scoreID);
		
		// Data returned from get query is the new score for this pimp
		$( scoreID ).html(data);
	});
});

$('.downvote').click( function() {
	var pimp_id;
	pimp_id = $(this).attr("data-pimp_id");
	$.get('/downvote/', { pimp_id : pimp_id }, function(data) {
		var scoreID = '#pimp_' + pimp_id + '_score';
		
		// Data returned from get query is the new score for this pimp
		$( scoreID ).html(data);
	});
});

// jQuery functions for following and unfollowing
$('.followButton').click( function() {
		var user_id;
		user_id = $(this).attr("data-user_id");
		$.get('/follow/', { user_id : user_id }, function(data) {
			var followClass = '.user_' + user_id + '_follow';
			
			$( followClass ).html(data);
	});
});