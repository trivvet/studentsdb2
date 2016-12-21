function initJournal() {
  var indicator = $('#ajax-progress-indicator'), modal2 = $('#modalAlert');
  
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
        $('input').prop('disabled', true);
        var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
        modal2.find('.modal-body').html(spinner);
        modal2.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
      });
      },
      'error': function(xhr, status, error) {
        alert(error);
        indicator.hide();
      },
      'success': function(data, status, xhr) {
        indicator.hide();
        $('input').prop('disabled', false);
        modal2.modal('hide');
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
  var defaultDate = $('input.dateinput').val();
  if (!defaultDate) {
    defaultDate = '1998-01-01'
  }
  $('input.dateinput').datetimepicker({
    'useCurrent': false,
    'format': 'YYYY-MM-DD',
    'viewDate': defaultDate
  }).on('dp.hide', function(event) {
    $(this).blur();
  });
  $('input.datetimeinput').datetimepicker({
    'format': 'YYYY-MM-DD HH:mm'
  }).on('dp.hide', function(event) {
    $(this).blur();
  });
}

function initForm(form, modal, link) {
  // attach datepicker
  initDateFields();

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event) {
    modal.modal('hide');
    return false;
  });

  var modal2 = $('#modalAlert');

  // make form work in AJAX mode
  form.ajaxForm({
    url: link.attr('href'),
    dataType: 'html',
    error: function() {
      modal.find('#modalAlert .').show();
      $('input, select, textarea').prop('disabled', false);
      return false;
    },
    beforeSend: function() {
      $('input, select, textarea').prop('disabled', true);
      var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
      modal2.find('.modal-body').html(spinner);
      modal2.modal({
        'keyboard': false,
        'backdrop': false,
        'show': true
      });
    },
    success: function(data, status, xhr) {
      var html = $(data), newform = html.find('#content-column form.form-horizontal');

      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));
      modal2.modal('hide');

      // copy form to modal if we found it in server repsonse
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initForm(newform, modal, link)
      } else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 second, so that user can read
        // success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}

function initFormPage() {
  $('a.form-link').click(function(){
    var link = $(this), modal2 = $('#modalAlert');
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'beforeSend': function() {
        var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
        $('.dropdown').removeClass('open');
        modal2.find('.modal-body').html(spinner);
        modal2.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'success': function(data, status, xhr) {
        if (status != 'success') {
          alert('Помилка на спрвері. Спробуйте будь-ласка пізніше');
          return False;
        }
        var modal = $('#myModal'), html = $(data),
            form = html.find('#content-column form');
        modal.find('.modal-title').html(html.find('#content-column h2'));
        modal.find('.modal-body').html(form);

        // init our edit form
        initForm(form, modal, link);
        
        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
        modal2.modal('hide');
      },
      'error': function() {
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
        return false;
      }
    });

    return false;
  });
}

function initSubHeaderNav() {
  $('.nav-tabs a').click(function() {
    var link = $(this), modal2 = $('#modalAlert');
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'beforeSend': function() {
        var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
        $('.dropdown').removeClass('open');
        modal2.find('.modal-body').html(spinner);
        modal2.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'success': function(data, status, xhr) {
        var html = $(data), newpage = html.find('#content-column');
        $('.nav-tabs li.active').removeClass('active');
        link.parent('li').addClass('active');
        link.blur();
        $('#content-column').html(newpage);
        modal2.modal('hide');
  
        initFunctions();
        initJournal();
        initDropDownNav();
      },
      'error': function() {
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
        return false;
      }
    });
    return false;
  });
}

function initDropDownNav() {
  $('#journalNavigate').click(function() {
    var link = $(this), modal2 = $('#modalAlert');
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'beforeSend': function() {
        var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
        $('.dropdown').removeClass('open');
        modal2.find('.modal-body').html(spinner);
        modal2.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'success': function(data, status, xhr) {
        var html = $(data), newpage = html.find('#content-column');
        $('.nav-tabs li.active').removeClass('active');
        link.parent('li').addClass('active');
        link.blur();
        $('#content-column').html(newpage);
        modal2.modal('hide');
  
        initFunctions();
        initJournal();
      },
      'error': function() {
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
        return false;
      }
    });
    return false;
  });
}

function initOrderBy() {
  $('th a').click(function(){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr) {
        var newpage = $(data).find('table').children(),
            newpaginate = $(data).find('nav').children();
        $('table').html(newpage);
        $('nav').html(newpaginate);

        initFunctions();
      }
    });
    return false;
  });
}

function initPaginate() {
    $('.pagination a').click(function() {
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr) {
        var html = $(data), newpage = html.find('tbody').children();
        $('.pagination li.active').removeClass('active');
        if (link.attr('aria-label') == 'Previous') {
          $('.pagination li:nth-child(2)').addClass('active');
        } else if (link.attr('aria-label') == 'Next') {
          $('.pagination li:nth-last-child(2)').addClass('active');
        } else {
          link.parent('li').addClass('active');
        }
        link.blur();
        $('tbody').html(newpage);

        initFormPage();
        initOrderBy();
        initDropDownNav();
        initJournal();
      }
    });
    return false;
  });
}

function initFunctions() {
  initFormPage();
  initOrderBy();
  initPaginate();
  initDropDownNav()
}

$(document).ready(function(){
  initGroupSelector();
  initDateFields();
  initSubHeaderNav();
  initFunctions();
})