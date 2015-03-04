// Code to redirect login/registration pages
function redirect( url ) {
	console.log('tes2');
	setTimeout( function() {
		console.log('test3');
		window.location.href = url;
	}, 5000 ); // Redirect after 5 seconds
}