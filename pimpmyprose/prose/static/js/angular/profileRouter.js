// Router for the profile page, to show prose or pimps of user
mainApp.config( [ '$routeProvider',
	function( $routeProvider ) {
		$routeProvider.
			when( '/prose', {
				templateUrl: 'prose.html',
				controller: 'proseController'
			} ).
			when( '/pimps', {
				templateUrl: 'pimps.html',
				controller: 'pimpsController'
			} ).
			otherwise( {
				redirectTo: '/prose'
			} );
	}
] );
