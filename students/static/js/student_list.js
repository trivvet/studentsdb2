$(document).ready(function(){
  
  $('#add_page').click(function(){
    $.ajax({
      url: $(this).attr('href'),
      success: function(result){
        var trLast = $('tbody tr:last-child').clone();
        trLast.children('td:nth-child(1)').html('1');
        $('tbody tr:last-child').after(trLast);
        for (r in result){
          console.log(r['id']);
        }
        console.log(result);
      }
    });  
  });
  
});
