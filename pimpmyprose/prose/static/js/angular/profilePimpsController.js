// Assign a controller for getting the parent prose and all pimps in a detail
mainApp.controller( 'profilePimpsController', function( $scope, $http, queryFactory ) {
  // Assign global URL for profiles into scope
  $scope.profileURL = profileURL;

  // Function which sets the Pimps
  var setPimps = function( pimpURL ) {
    $http.get( pimpURL ).success( function( response ) {
      $scope.pimps = response;
      console.log( response );
      $scope.numPages = Math.ceil( response.count / 10 );

      // Get all query parameters
      var queryParams = queryFactory.getParams( pimpURL );

      // Get the page number from the query parameters
      if ( "page" in queryParams ) {
        $scope.currentPage = queryParams[ "page" ];
      } else {
        $scope.currentPage = 1;
      }

    } );
  }

  $scope.pimps = { results : [] };
  // Get page 1 of all pimps associated with this Prose, default ordering is top
  var pimpURL = pimpAPI + '?user_id=' + user_id;
  setPimps( pimpURL );

  // Function which takes ordering parameter and reloads all pimps on page
  $scope.setOrder = function( order ) {
    $scope.currentOrderBy = order;

    // Query parameter requires order word to be lowercase
    var orderedPimpURL = pimpURL + '&orderBy=' + order.toLowerCase();
    console.log( orderedPimpURL );
    setPimps( orderedPimpURL );
  }

  $scope.orderBy_set = [
    'Top',
    'New',
    'Worst',
    'Old'
  ]

  // Initialize the current orderBy
  $scope.currentOrderBy = $scope.orderBy_set[0];

  // Get next page
  $scope.nextPage = function() {
    if ( $scope.pimps.next !== null ) {
      var pimpURL = $scope.pimps.next;
      setPimps( pimpURL );
    }
  }

  // Get previous page
  // Get next page
  $scope.previousPage = function() {
    if ( $scope.pimps.previous !== null ) {
      var pimpURL = $scope.pimps.previous;
      setPimps( pimpURL );
    }
  }

} );
