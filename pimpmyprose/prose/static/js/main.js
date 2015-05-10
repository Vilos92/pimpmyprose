// Code to redirect login/registration pages
function redirect( url ) {
	setTimeout( function() {
		window.location.href = url;
	}, 5000 ); // Redirect after 5 seconds
}