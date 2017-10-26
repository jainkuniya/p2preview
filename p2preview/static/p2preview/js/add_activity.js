var filePath = '';

$('#new_activity_form').submit(function() {
  var frm = $('#new_activity_form');
  var activity_name = $('#activity_name').val();
  var rubric_id = $('#rubric_id').val();
  var course_id = $('#course_id').val();
  var duration = $('#duration').val();
  var groupSize = $('#groupSize').val();

  if (filePath === '') {
    $('#id_error').text('Please upload image');
    return false;
  }

  if (rubric_id === '-1') {
    $('#id_error').text('Please select Rubric');
    return false;
  }

  if (course_id === '-1') {
    $('#id_error').text('Please select Course');
    return false;
  }

  $.ajax({
    type: 'post',
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', getCookie('token'));
    },
    url: '/api/v1/create_activity/',
    data: {
      activity_name: activity_name,
      file_path: filePath,
      rubric_id: rubric_id,
      course_id: course_id,
      duration: duration,
      groupSize: groupSize,
    },
    dataType: 'json',
    success: function(data) {
      if (data.success === 1) {
        $(location).attr('href', '/activity');
      } else if (data.success === -99) {
        clearLoginCookie();
      } else {
        $('#id_error').text(data.message);
      }
    },
  });
  return false;
});

Dropzone.options.myAwesomeDropzone = {
  init: function() {
    this.on('success', function(file, response) {
      if (response.success === 1) {
        filePath = response.data.url;
      }
    });
    this.on('removedfile', function(file, response) {
      filePath = '';
    });
  },
};

function toggleCheckbox(value, activity_id) {
  $.ajax({
    type: 'post',
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', getCookie('token'));
    },
    url: '/api/v1/toggle_activity_status/',
    data: {
      activity_id: activity_id,
      value: value,
    },
    dataType: 'json',
    success: function(data) {
      if (data.success === 1) {
        //$(location).attr('href', '/activity');
      } else if (data.success === -99) {
        clearLoginCookie();
      } else {
        alert(data.message);
        $(location).attr('href', '/activity');
      }
    },
  });
}
