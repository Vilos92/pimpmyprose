// Assign a controller for getting the parent prose and all pimps in a detail
mainApp.controller( 'detailController', function( $scope, $http ) {
  // Get page 1 of all pimps associated with this Prose
  var pimpURL = pimpAPI + '?prose_id=' + prose_id;
  $http.get( pimpURL ).success( function( response ) {
    $scope.pimps = response;
  } );

  // Initialize the ordering for this page, which will be by highest score
  $scope.orderby_set = [
    { title: 'Top', expression: 'downvotes - upvotes' },
    { title: 'New', expression: '-pub_date' },
    { title: 'Worst', expression: 'upvotes - downvotes' },
    { title: 'Old', expression: 'pub_date' }
  ];

  // Initialize the current Filter
  $scope.currentOrderby = $scope.orderby_set[0];

} );
