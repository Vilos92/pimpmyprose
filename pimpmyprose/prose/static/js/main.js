// Code to redirect login/registration pages
function redirect( url ) {
	setTimeout( function() {
		window.location.href = url;
	}, 5000 ); // Redirect after 5 seconds
}

// Count charcters in Prose/Pimp Textarea
// Change value of remainingCharacters div to amount of characters remaining
function getRemainingCharacters( textarea ) {
	var remainingCharacters = textarea.maxLength - textarea.value.length;

	$( '#remainingCharacters' ).text( remainingCharacters + ' characters remaining.' );
}
