$(document).ready(function() {

$('input#name').on('focusout', function () {
    $.getJSON('/checkname', {
      name: $('#name').val(),
    }, function(data) {
      $("#result").text(data.result);
    });
  return false;
  });

});






