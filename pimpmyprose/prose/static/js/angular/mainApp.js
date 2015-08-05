// Create module for the main pimpMyProse Angular application
var mainApp = angular.module( "mainApp", [] );

// Change the interpolation syntax, as to not collide with django
mainApp.config( function( $interpolateProvider ) {
	$interpolateProvider.startSymbol( '{[{' );
	$interpolateProvider.endSymbol( '}]}' );
} );
