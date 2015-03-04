// jQuery functions for voting
$('.upvote').click( function() {
	var pimp_id;
	pimp_id = $(this).attr("data-pimp_id");
	$.get('/prose/upvote/', { pimp_id : pimp_id }, function(data) {
		var scoreID = '#pimp_' + pimp_id + '_score';
		console.log(scoreID);
		
		// Data returned from get query is the new score for this pimp
		$( scoreID ).html(data);
	});
});

$('.downvote').click( function() {
	var pimp_id;
	pimp_id = $(this).attr("data-pimp_id");
	$.get('/prose/downvote/', { pimp_id : pimp_id }, function(data) {
		var scoreID = '#pimp_' + pimp_id + '_score';
		
		// Data returned from get query is the new score for this pimp
		$( scoreID ).html(data);
	});
});

function test() {
	console.log('Whatup');
}

// Code to redirect login/registration pages
function redirect( url ) {
	console.log('tes2');
	setTimeout( function() {
		console.log('test3');
		window.location.href = url;
	}, 5000 ); // Redirect after 5 seconds
}