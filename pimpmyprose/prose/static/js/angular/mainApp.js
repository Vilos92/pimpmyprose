// Create module for the main pimpMyProse Angular application
var mainApp = angular.module( "mainApp", [ 'ngRoute' ] );

// Change the interpolation syntax, as to not collide with django
mainApp.config( function( $interpolateProvider ) {
	$interpolateProvider.startSymbol( '{[{' );
	$interpolateProvider.endSymbol( '}]}' );
} );

// Factory to return query parameters from a URL string
mainApp.factory( 'queryFactory', function() {
	return {
		// Return parameters from a query
		getParams : function( query ) {
			var vars = [], hash
			var hashes = query.slice( query.indexOf( '?' ) + 1 ).split( '&' );

			for ( var i = 0; i < hashes.length; ++i ) {
				hash = hashes[i].split( '=' );
				vars.push( hash[0] );
				vars[ hash[0] ] = hash[1];
			}

			return vars;
		}
	}
} );
