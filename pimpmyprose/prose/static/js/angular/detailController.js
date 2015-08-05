// Assign a controller for getting the parent prose and all pimps in a detail
mainApp.controller( 'detailController', function( $scope, $http ) {
  // Assign global URL for profiles into scope
  $scope.profileURL = profileURL;

  // Function which sets the Pimps
  var setPimps = function( pimpURL ) {
    $http.get( pimpURL ).success( function( response ) {
      $scope.pimps = response;
    } );
  }

  $scope.pimps = { results : [] };
  // Get page 1 of all pimps associated with this Prose
  var pimpURL = pimpAPI + '?prose_id=' + prose_id;
  setPimps( pimpURL );

  // Initialize the ordering for this page, which will be by highest score
  $scope.orderby_set = [
    { title: 'Top', expression: 'downvotes - upvotes' },
    { title: 'New', expression: '-pub_date' },
    { title: 'Worst', expression: 'upvotes - downvotes' },
    { title: 'Old', expression: 'pub_date' }
  ];

  // Initialize the current Filter
  $scope.currentOrderby = $scope.orderby_set[0];

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
