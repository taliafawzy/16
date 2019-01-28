$( ".checkers" ).on( "click", function() {
  if($( ".checkers:checked" ).length >= 1)
  {
  	$('#submitbtn').prop('disabled', false);
  }
  else
  {
  	$('#submitbtn').prop('disabled', true);
  }
});
