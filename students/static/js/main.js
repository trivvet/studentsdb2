function initJournal() {
  var indicator = $('#ajax-progress-indicator');
  
  $('.day-box input[type="checkbox"]').click(function(event){
    var box = $(this)
    $.ajax(box.data('url'), {
      'type': 'POST',
      'async': true,
      'dataType': 'json',
      'data': {
        'pk': box.data('student-id'),
        'date': box.data('date'),
        'present': box.is(':checked') ? '1' : '',
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      'beforeSend': function(xhr, setting){
        indicator.show();
      },
      'error': function(xhr, status, error) {
        alert(error);
        indicator.hide();
      },
      'success': function(data, status, xhr) {
        indicator.hide();
      }
    });
  });
}

function initGroupSelector() {
  // look up select element with groups and attach our even handler
  // on field "change" event
  $('#group-selector select').change(function(event){
    var group = $(this).val()

    if (group) {
      // set cookie with expiration date 1 year since now;
      // cookie creation function takes period in days
      Cookies.set('current_group', group, {'path': '/', 'expires': 365});
    } else {
      // otherwise we delete the cookie
      Cookies.remove('current_group', {'path': '/'})
    }

    // end reload a page
    location.reload(true)

    return true;
  });
}

function initDateFields() {
  $('input.dateinput').datetimepicker({
    'format': 'YYYY-MM-DD'
  }).on('dp.hide', function(event) {
    $(this).blur();
  });
}

$(document).ready(function(){
  initJournal();
  initGroupSelector();
  initDateFields();
})
