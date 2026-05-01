$(document).ready(function() {
  console.log("Document Ready");
  
  // Remove the alert after 3 seconds
  setTimeout(function() {
    $('#alert').hide();
  }, 3000);

  $('#categorySelect').on('change', function(){
    getCategoryItems($(this).val());
  });

  function getCategoryItems(categoryId) {
    $.ajax({
      type: 'GET',
      url: '/category/items/' + categoryId,
      success: function(data) {
        $('#itemsList').html(data);
      },
      error: function(xhr, status, error) {
        alert('No items available for this category');
      }
    });
  }
});