// Assign a controller for getting the parent prose and all prose in a detail
mainApp.controller( 'proseController', function( $scope, $http, queryFactory ) {
  // Assign global URLs into scope
  $scope.profileURL = profileURL;
  $scope.proseURL = proseURL;

  // Check if page wants to hide link to parent proses on prose (details page)
  if ( typeof hideParentLink !== 'undefined' ) {
    $scope.hideParentLink = hideParentLink;
  }

  // Function which sets the prose
  var setProse = function( proseURL ) {
    $http.get( proseURL ).success( function( response ) {
      $scope.prose = response;
      $scope.numPages = Math.ceil( response.count / 10 );

      // Get all query parameters
      var queryParams = queryFactory.getParams( proseURL );

      // Get the page number from the query parameters
      if ( "page" in queryParams ) {
        $scope.currentPage = queryParams[ "page" ];
      } else {
        $scope.currentPage = 1;
      }

    } );
  }

  $scope.prose = { results : [] };
  // Get page 1 of all prose associated with this Prose, default ordering is top
  var proseURL = proseAPI + proseQueryParameter;
  setProse( proseURL );

  // Function which takes ordering parameter and reloads all prose on page
  $scope.setOrder = function( order ) {
    $scope.currentOrderBy = order;

    // Query parameter requires order word to be lowercase
    var orderedProseURL = proseURL + '&orderBy=' + order.toLowerCase();
    setProse( orderedProseURL );
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
    if ( $scope.prose.next !== null ) {
      var proseURL = $scope.prose.next;
      setProse( proseURL );
    }
  }

  // Get previous page
  // Get next page
  $scope.previousPage = function() {
    if ( $scope.prose.previous !== null ) {
      var proseURL = $scope.prose.previous;
      setProse( proseURL );
    }
  }

} );
