// run when click on chechbox
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
        $('#content-column .alert').removeClass('alert-info')
            .addClass('alert-danger').html('Помилка на сервері (код - ' + error + '). Спробуйте пізніше');
        modal2.modal('hide');
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
    var link = $('.nav-tabs li.active a');
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr) {
        var html = $(data), newpage = html.find('#content-column').children();
        link.blur();
        $('#content-column').html(newpage);

        initFunctions();
        initJournal();
      }
    });

    return false;
  });
}

function initDateFields() {
  var defaultDate = $('input.dateinput').val(),
      calendarButton = "<span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span>";
      timeButton = "<span class='input-group-addon'><span class='glyphicon glyphicon-time'></span>";
  if (!defaultDate) {
    defaultDate = '1998-01-01'
  }
  $('input.dateinput').datetimepicker({
    'useCurrent': false,
    'format': 'YYYY-MM-DD',
    'viewDate': defaultDate,
    'toolbarPlacement': 'bottom',
    'allowInputToggle': true,
    'locale': 'uk'
  }).on('dp.hide', function(event) {
    $(this).blur();
  }).wrap('<div></div>').after(calendarButton).parent().addClass('input-group date');
  $('input.datetimeinput').datetimepicker({
    'format': 'YYYY-MM-DD HH:mm',
    'stepping': 15,
    'daysOfWeekDisabled': [6, 0],
    'toolbarPlacement': 'bottom',
    'disabledHours': [0, 1, 2, 3, 4, 5, 6, 7, 8, 21, 22, 23, 24],
    'locale': 'uk'
  }).on('dp.hide', function(event) {
    $(this).blur();
  }).wrap('<div></div>').after(timeButton).parent().addClass('input-group date');;
  $('.input-group-addon').click(function(){
    $(this).siblings('input').focus();
  });
}

// use when form is post
function initForm(form, modal, link) {
  // attach datepicker
  initDateFields();

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event) {
    modal.modal('hide');
    $('input, select, textarea').removeAttr('disabled');
    return false;
  });

  modal.find('button.close').click(function(event){
    $('input,select, textarea').removeAttr('disabled');
  });

  var modal2 = $('#modalAlert');

  // make form work in AJAX mode
  form.ajaxForm({
    url: link.attr('href'),
    dataType: 'html',
    error: function() {
      $('input, select, textarea').prop('disabled', false);
      modal2.modal('hide');
      modal.find('.modal-body').html('<div class="alert alert-danger">"Виникла помилка на сервері. Будь-ласка спробуйте пізніше"</div>');
      setTimeout(function() {
          modal.modal('hide');
        }, 1500);
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
        setTimeout(function() {
          $('#sub-header').html(html.find('#sub-header div'));
          $('#content-column').html(html.find('#content-column'));
          modal.modal('hide');
          initSubHeaderNav();
          initFunctions();
          initResultPage();
          
        }, 1000);

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

function initContactForm() {
  $('#submit-id-send_button').click(function(){
    var link = $("#contact-link"), form = $('form');
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'method': 'post',
      'error': function() {
        $('input, select, textarea').prop('disabled', false);
        modal2.modal('hide');
        $('h2').after('<div class="alert alert-danger">"Виникла помилка на сервері. Будь-ласка спробуйте пізніше"</div>');
        return false;
      },
      'beforeSend': function() {
        $('input, select, textarea').prop('disabled', true);
        var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
        modal2.find('.modal-body').html(spinner);
        modal2.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'success': function(data, status, xhr) {
        $('h2').after('<div class="alert alert-danger">"Виникла помилка на сервері. Будь-ласка спробуйте пізніше"</div>');
        modal2.modal('hide');

        // initialize form fields and buttons
        initContactForm()
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
        initResultPage()
        $('.contact-form').attr('action', $("#contact-link").attr('href'))
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
  $('.journalNavigate').click(function() {
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
            newpaginate = $(data).find('nav').children(),
            newbutton = $(data).find('#buttonLoadMore');
        $('table').html(newpage);
        $('nav').html(newpaginate);
        $('.buttonLoad').html(newbutton);

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
        var html = $(data), newpage = html.find('tbody').children(), newbutton = html.find('#buttonLoadMore');
        $('.pagination li.active').removeClass('active');
        if (link.attr('aria-label') == 'Previous') {
          $('.pagination li:nth-child(2)').addClass('active');
        } else if (link.attr('aria-label') == 'Next') {
          $('.pagination li:nth-last-child(2)').addClass('active');
        } else {
          link.parent('li').addClass('active');
        }
        if (newbutton) {
          link.blur();
          $('#buttonLoadMore').remove();
          $('.buttonLoad').html(newbutton);
          loadMore();
        } else {
          $('#buttonLoadMore').remove();
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

function loadMore() {
  $('#buttonLoadMore').click(function() {
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr) {
        var html = $(data), newpage = html.find('tbody').children(), newbutton = html.find('#buttonLoadMore').attr('href');
        $('tbody').append(newpage);
        if (newbutton) {
          link.blur();
          $('#buttonLoadMore').attr('href', newbutton);
        } else {
          $('#buttonLoadMore').remove();
        }
        $('ul.pagination').remove();
        
        $('a.form-link').off();
        initFormPage();
      }
    });
    return false;
  });
}

function initResultPage() {
  $('a.results-link').click(function(){
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
          alert('Помилка на сервері. Спробуйте будь-ласка пізніше');
          return False;
        }
        var modal = $('#myModal'), html = $(data),
            newpage = html.find('#content-column');
        modal.find('.modal-title').html(html.find('#content-column h2'));
        modal.find('.modal-body').html(newpage);
        
        modal.modal({
          'keyboard': true,
          'backdrop': true,
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


function initFunctions() {
  initFormPage();
  initOrderBy();
  initPaginate();
  initDropDownNav();
  loadMore();
}

$(document).ready(function(){
  initGroupSelector();
  initDateFields();
  initSubHeaderNav();
  initFunctions();
  initResultPage()
})
