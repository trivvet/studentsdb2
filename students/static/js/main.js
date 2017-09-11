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
            .addClass('alert-danger').html(gettext('There was an error on the server') + gettext('(code - ') + error + gettext('). Please, try again later'));
        modal2.modal('hide');
        indicator.hide();
      },
      'success': function(data, status, xhr) {
        indicator.hide();
        if (data.status == 'error') {
          if (box[0].checked) {
            box[0].checked = false;
          } else {
            box[0].checked = true;
          }
          alert(data.message);
        }
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
        initFormPage();
        initFormPageDelete();
      }
    });

    return false;
  });
}

function initLanguageSelector() {
  $('#lang-selector button').click(function(event){
    var language = $(this).val()

    // set cookie with expiration date 1 year since now;
    // cookie creation function takes period in days
    Cookies.set('django_language', language, {'path': '/', 'expires': 365});

    // and reload a page
    location.reload();
  });
}

function initDateFields() {
  var defaultDate = $('input.dateinput').val(),
      calendarButton = "<span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span>",
      timeButton = "<span class='input-group-addon'><span class='glyphicon glyphicon-time'></span>",
      currentLanguage = $("#cur-lang").html();
  if (!defaultDate) {
    defaultDate = '1998-01-01'
  }
  $('input.dateinput').datetimepicker({
    'useCurrent': false,
    'format': 'YYYY-MM-DD',
    'viewDate': defaultDate,
    'toolbarPlacement': 'bottom',
    'allowInputToggle': true,
    'locale': currentLanguage
  }).on('dp.hide', function(event) {
    $(this).blur();
  }).wrap('<div></div>').after(calendarButton).parent().addClass('input-group date');
  if ($('#id_log_datetime').length > 0) {
    $('#id_log_datetime').datetimepicker({
      'format': 'YYYY-MM-DD HH:mm',
      'useCurrent': false,
      'toolbarPlacement': 'bottom',
      'locale': currentLanguage
    }).on('dp.hide', function(event) {
      $(this).blur();
    });
  } else {
    $('input.datetimeinput').datetimepicker({
      'format': 'YYYY-MM-DD HH:mm',
      'stepping': 15,
      'daysOfWeekDisabled': [6, 0],
      'toolbarPlacement': 'bottom',
      'disabledHours': [0, 1, 2, 3, 4, 5, 6, 7, 8, 21, 22, 23, 24],
      'locale': currentLanguage
    }).on('dp.hide', function(event) {
      $(this).blur();
    }).wrap('<div></div>').after(timeButton).parent().addClass('input-group date');
  }
  $('.input-group-addon').click(function(){
    $(this).siblings('input').focus();
  });
}

function initPhotoView() {
  $('#id_photo').on('change', function(){
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        $('#photo-preview').remove();
        $(this).after("<img id='photo-preview' alt='photo' src='#' class='img-circle' width='100' height='100'>")
        reader.onload = function (e) {
            $('#photo-preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(this.files[0]);
    }
  });
  if ($('#id_photo').siblings('a').length > 0) {
    var reader = new FileReader();
    $('#photo-clear_id').before("<img id='photo-preview' alt='photo' src='#' class='img-circle' width='100' height='100'>")
    $('#photo-preview').attr('src', $('#id_photo').siblings('a').attr('href'));
  }
}

// use when form is post
function initForm(form, modal, link) {
  // attach datepicker
  initDateFields();
  initPhotoView();
  initPasswordForgotView();

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event) {
    form.ajaxForm({
      url: link,
      dataType: 'html',
      error: function() {
        $('input, select, textarea').prop('disabled', false);
        modal2.modal('hide');
        modal.find('.modal-body').html('<div class="alert alert-danger">"' + gettext('There was an error on the server. Please try again later') + '"</div>');
        setTimeout(function() {
          modal.modal('hide');
        }, 1500);
        History.pushState({'page': 'openForm'}, $('#content-column h2').text(), $('#sub-header li.active a').attr('href'));
        return false;
      },
      success: function(data, status, xhr) {
        var html = $(data), message = html.find('div.alert-warning');
        $('div.alert-warning').remove();
        $('#content-column').prepend(message);
        modal.modal('hide');
        $('input, select, textarea').removeAttr('disabled');
        History.pushState({'page': ''}, $('#content-column h2').text(), $('#sub-header li.active a').attr('href'));
      }
    });
  });

  modal.find('button.close').click(function(event){
    $('input,select, textarea').removeAttr('disabled');
    History.pushState({'page': ''}, $('#content-column h2').text(), $('#sub-header li.active a').attr('href'));
  });

  var modal2 = $('#modalAlert');

  // make form work in AJAX mode
  form.ajaxForm({
    url: link,
    dataType: 'html',
    error: function() {
      $('input, select, textarea').prop('disabled', false);
      modal2.modal('hide');
      modal.find('.modal-body').html('<div class="alert alert-danger">"' + gettext('There was an error on the server. Please try again later') + '"</div>');
      setTimeout(function() {
          modal.modal('hide');
        }, 3000);
      History.pushState({'page': 'openForm'}, $('#content-column h2').text(), $('#sub-header li.active a').attr('href'));
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
      modal.find('.modal-body').html(html.find('.alert-danger, .alert-warning, .alert-success'));
      modal2.modal('hide');

      // copy form to modal if we found it in server repsonse
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initForm(newform, modal, link)
      } else {
        // if no form, it means success and we need to reload page
        // to get updated page;
        // reload after 2 second, so that user can read
        // success message
        if (link == '/user-auth/' || link == '/user-preference/' || link == '/users/login/') {
          setTimeout(function() {
            location.replace('/');
          }, 2500);
        } else if (link == '/register/registration/') {
          modal.find('.modal-title').html(html.find('#content-column h2'));
          modal.find('.modal-body').html(html.find('#content-column p'));
          setTimeout(function() {
            location.replace('/');
          }, 4000);
        } else if (link == '/') {
          location.replace('/');
        } else if (link =='/password/reset/' || link=='/users/password/change/') {
          $('#sub-header').html(html.find('#sub-header div'));
          $('#content-column').html(html.find('#content-column'));
          $('#group-selector').html(html.find('#group-selector select'));
          $('input, select, textarea').prop('disabled', false);
          modal.modal('hide');
          initSubHeaderNav();
          initFunctions();
        } else {
          setTimeout(function() {
            $('#sub-header').html(html.find('#sub-header div'));
            $('#content-column').html(html.find('#content-column'));
            $('#group-selector').html(html.find('#group-selector select'));
            $('input, select, textarea').prop('disabled', false);
            modal.modal('hide');
            initSubHeaderNav();
            initFunctions();
            initResultPage();
            initFormPage();
            initFormPageDelete();
          }, 2000);
        }
      }
//      $('a.form-link').off();
      History.pushState({'page': 'openForm'}, $('#content-column h2').text(), $('#sub-header li.active a').attr('href'));
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
          alert(gettext('There was an error on the server. Please try again later'));
          return false;
        }
        var modal = $('#myModal'), html = $(data),
            form = html.find('#content-column form');
        if (html.find('div.alert-warning').length != 0) {
            $('#sub-header').after(html.find('div.alert-warning'));
            modal2.modal('hide');
            return false;
        }
        modal.find('.modal-title').html(html.find('#content-column h2'));
        modal.find('.modal-body').html(form);
        modal.find('.modal-body').prepend(html.find('#select-language'));
        modal.find('.modal-footer').html(html.find('#content-column p'));

        // init our edit form
        initForm(form, modal, link.attr('href'));
        initLanguageFormPage();

        History.pushState({'page': 'openForm'}, $('#myModal h2').text(), link.attr('href'));
        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
        modal2.modal('hide');
      },
      'error': function() {
        alert(gettext('There was an error on the server. Please try again later'));
        return false;
      }
    });

    return false;
  });
}

function initLanguageFormPage() {
  $('#select-language a').click(function(){
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
          alert(gettext('There was an error on the server. Please try again later'));
          return False;
        }
        var modal = $('#myModal'), html = $(data),
            form = html.find('#content-column form');
        modal.find('.modal-body').html(form);
        modal.find('.modal-body').prepend(html.find('#select-language'));

        // init our edit form
        initForm(form, modal, link.attr('href'));
        initLanguageFormPage();

        History.pushState({'page': 'openForm'}, $('#myModal h2').text(), link.attr('href'));
        modal2.modal('hide');
      },
      'error': function() {
        alert(gettext('There was an error on the server. Please try again later'));
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
        $('h2').after('<div class="alert alert-danger">"' + gettext('There was an error on the server. Please try again later') + '"</div>');
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
        $('h2').after('<div class="alert alert-danger">"' + gettext('There was an error on the server. Please try again later') + '"</div>');
        modal2.modal('hide');

        // initialize form fields and buttons
        initContactForm()
      }
    });
    return false;
  });
}

function SubHeaderNavigation(link, pagination) {
  var modal2 = $('#modalAlert');
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
        var html = $(data), newpage = html.find('#content-columns');
        $('#sub-header li.active').removeClass('active');
        link.parent('li').addClass('active');
        link.blur();

        $('#content-column').html(newpage);
        modal2.modal('hide');
        $('div.alert-warning div.alert-danger').remove();

        initFunctions();
        initResultPage();
        initFormPage();
        $('.contact-form').attr('action', $("#contact-link").attr('href'));
        if (pagination == false) {
          History.pushState({'page': 'nav', 'url': link.attr('href')}, $('#content-column h2').text(), link.attr('href'));
        } else {
          var data = location.search, dataurl = location.pathname,    linkurl = "[href='" + dataurl + data + "']", link2 = $(linkurl);
          if (link2.length > 0 && link2.parent().is('th')) {
            OrderByNavigation(link2);
          } else if (link2.length > 0) {
            PageNavigation(link2);
          } else {
            $.ajax({
              'url': dataurl + data,
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
          }
        }
      },
      'error': function() {
        alert(gettext('There was an error on the server. Please try again later'));
        return false;
      }
    });
}

function initSubHeaderNav() {
  $('.nav-tabs a').click(function() {
    SubHeaderNavigation($(this), false);
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
        History.pushState({}, gettext('Student Visiting'), link.attr('href'));
      },
      'error': function() {
        alert(gettext('There was an error on the server. Please try again later'));
        return false;
      }
    });
    return false;
  });
}

function OrderByNavigation(link) {
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

      History.pushState({'page': 'orderby', 'url': link.attr('href')}, $('#content-column h2').text(), link.attr('href'));

      initFunctions();
      initFormPage();
    }
  });
}

function initOrderBy() {
  $('th a').click(function(){
    var link = $(this);
    OrderByNavigation(link);
    return false;
  });
}

function PageNavigation(link) {
  if (link.length > 1) {
    link = link.first();
  }
  $.ajax({
    'url': link.attr('href'),
    'dataType': 'html',
    'type': 'get',
    'success': function(data, status, xhr) {
      var html = $(data), newpage = html.find('tbody').children(), newbutton = html.find('#buttonLoadMore');
      $('.pagination li.active').removeClass('active');
      if (link.attr('aria-label') == 'Previous') {
        $('.pagination li:nth-child(2)').addClass('active');
      } else if (link.attr('aria-label') == 'Next' || link.is('.btn')) {
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

      initOrderBy();
      initDropDownNav();
      initFormPage();

      History.pushState({'page': 'pagenav', 'url': link.attr('href')}, $('#content-column h2').text(), link.attr('href'));
    }
  });
}

function initPaginate() {
  $('.pagination a').click(function() {
    var link = $(this);
    PageNavigation(link);
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
        $('.pagination li.active').next().addClass('active');

        $('a.form-link').off();
        $(':checkbox').off();
        $('.journalNavigate').off();
        $('.result-link').off();
        initFormPage();
        initJournal();
        initDropDownNav();
        initResultPage();
        initFormPageDelete()
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
          alert(gettext('There was an error on the server. Please try again later'));
          return false;
        }
        var modal = $('#myModal'), html = $(data),
            newpage = html.find('#content-column');
        modal.find('.modal-title').html(html.find('#content-column h2'));
        modal.find('.modal-footer').html(html.find('#info-change'));
        modal.find('.modal-body').html(newpage);

        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
        modal2.modal('hide');
      },
      'error': function() {
        alert(gettext('There was an error on the server. Please try again later'));
        return false;
      }
    });

    return false;
  });
}

function initPasswordForgotView() {
  $('#forgot-password').click(function(){
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
          alert(gettext('There was an error on the server. Please try again later'));
          return false;
        }
        var modal = $('#myModal'), html = $(data),
            newpage = html.find('#content-column');
            form = html.find('#content-column form');
        modal.find('.modal-title').html(html.find('#content-column h2'));
        modal.find('.modal-body').html(newpage);

        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });

        initForm(form, modal, link.attr('href'));
        modal2.modal('hide');
      },
      'error': function() {
        alert(gettext('There was an error on the server. Please try again later'));
        return false;
      }
    });

    return false;
  });
}

function initBackButton() {
  $(window).on('popstate', function(event) {
    if (event.bubbles) {
      var State = History.getState(), data = State.data;
      if (data.page != 'openForm') {
        if ($('#myModal').attr('style') == 'display: block;') {
          $('#myModal').modal('hide');
        } else {
          if (data.page == 'nav') {
            var linkurl = "[href='" + data.url + "']", link = $(linkurl);
            SubHeaderNavigation(link, false);
          } else if (data.page == 'orderby') {
            var linkurl = "[href='" + data.url + "']", link = $(linkurl);
            if ($('#sub-header li.active a').attr('href') == location.pathname) {
              OrderByNavigation(link);
            } else {
              var linkurl2 = "[href='" + location.pathname + "']", link2 = $(linkurl2);
              SubHeaderNavigation(link2, '1');
            }
          } else if (data.page == 'pagenav') {
            var linkurl = "[href='" + data.url + "']", link = $(linkurl);
            if ($('#sub-header li.active a').attr('href') == location.pathname) {
              PageNavigation(link);
            } else {
              var linkurl2 = "[href='" + location.pathname + "']", link2 = $(linkurl2);
              SubHeaderNavigation(link2, '1');
            }
          } else {
            var link = State.url, modal2 = $('#modalAlert');
            $.ajax({
              'url': link,
              'dataType': 'html',
              'type': 'get',
              'beforeSend': function() {
                var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
                modal2.find('.modal-body').html(spinner);
                modal2.modal({
                  'keyboard': false,
                  'backdrop': false,
                  'show': true
                });
              },
              'success': function(data, status, xhr) {
                if (status != 'success') {
                  alert(gettext('There was an error on the server. Please try again later'));
                  return False;
                }
                var html = $(data), modal = $('#myModal');
                $('#sub-header').html(html.find('#sub-header'));
                $('#content-columns').html(html.find('#content-columns'));
                if (modal.attr('style')) {
                  modal.modal('hide');
                }
                initDateFields();
                initSubHeaderNav();
                initFunctions();
                initResultPage();
                modal2.modal('hide');
              },
              'error': function() {
                alert(gettext('There was an error on the server. Please try again later'));
                return false;
              }
            });
          }
        }
      } else {
        var link = State.url, modal2 = $('#modalAlert');
        $.ajax({
          'url': link,
          'dataType': 'html',
          'type': 'get',
          'beforeSend': function() {
            var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
            modal2.find('.modal-body').html(spinner);
            modal2.modal({
              'keyboard': false,
              'backdrop': false,
              'show': true
            });
          },
          'success': function(data, status, xhr) {
            if (status != 'success') {
              alert(gettext('There was an error on the server. Please try again later'));
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
            alert(gettext('There was an error on the server. Please try again later'));
            return false;
          }
        });
      }
    }
  });
}

function initFormPageDelete() {
  var modal2 = $('#modalAlert'), form = $('#change-student-list'),
    modal = $('#myModal');
  form.ajaxForm({
    url: form.attr('action'),
    dataType: 'html',
    error: function() {
      $('input, select, textarea').prop('disabled', false);
      modal2.modal('hide');
      modal.find('.modal-body').html('<div class="alert alert-danger">"' + gettext('There was an error on the server. Please try again later') + '"</div>');
      setTimeout(function() {
          modal.modal('hide');
        }, 3000);
      History.pushState({'page': 'openForm'}, $('#content-column h2').text(), $('#sub-header li.active a').attr('href'));
      return false;
    },
    beforeSend: function() {
      var spinner = '<i class="fa fa-refresh fa-spin" style="font-size:50px"></i>';
      $('.dropdown').removeClass('open');
      modal2.find('.modal-body').html(spinner);
      modal2.modal({
        'keyboard': false,
        'backdrop': false,
        'show': true
      });
    },
    success: function(data, status, xhr) {
      if (status != 'success') {
        alert(gettext('There was an error on the server. Please try again later'));
        return false;
      }
      var modal = $('#myModal'), html = $(data),
        form = html.find('#content-column form'),
        alertWarning = html.find('div.alert-warning'),
        alertDanger = html.find('#content-columns div.alert-danger');
      if (alertWarning.length != 0) {
        $('#sub-header').after(alertWarning);
        modal2.modal('hide');
        return false;
      } else if (alertDanger.length != 0) {
        $('#sub-header').after(alertDanger);
        modal2.modal('hide');
        return false;
      }
      modal.find('.modal-title').html(html.find('#content-column h2'));
      modal.find('.modal-body').html(form);

      // init our edit form
      initForm(form, modal, form.attr('action'));

      History.pushState({'page': 'openForm'}, $('#myModal h2').text(), form.attr('action'));
      modal.modal({
        'keyboard': false,
        'backdrop': false,
        'show': true
      });
      modal2.modal('hide');
    }
  });
}

function initFunctions() {
  initOrderBy();
  initPaginate();
  initDropDownNav();
  loadMore();
  initJournal();
  initResultPage();
  initGroupSelector();
}

$(document).ready(function(){
  initFormPage();
  initFormPageDelete();
  initDateFields();
  initSubHeaderNav();
  initFunctions();
  initResultPage();
  initBackButton();
  initLanguageSelector()
})
