var filePath = [];
var textOrImage = 'False';

$('#new_activity_form').submit(function() {
  var frm = $('#new_activity_form');
  var activity_name = $('#activity_name').val();
  var rubric_id = $('#rubric_id').val();
  var course_id = $('#course_id').val();
  var duration = $('#duration').val();
  var groupSize = $('#groupSize').val();

  if (rubric_id === '-1') {
    alert('Please select Rubric');
    return false;
  }

  if (course_id === '-1') {
    alert('Please select Course');
    return false;
  }

  if (activity_name.length === 0) {
    alert('Please enter activity name');
    return false;
  }

  if (duration.length === 0) {
    alert('Please enter activity duration');
    return false;
  }

  if (groupSize.length === 0) {
    alert('Please enter group size');
    return false;
  }

  var texts = [];
  var i = 0;
  for (i = 0; i <= optionNumber; i++) {
    var text = $('#text' + i).val();
    if (text.length > 0) {
      texts = [...texts, { text: text, groupId: $('#groupId' + i).val() }];
    }
  }

  if (filePath.length === 0 && texts.length === 0) {
    alert('Please add image/text assigments');
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
      file_path: JSON.stringify(filePath),
      texts: JSON.stringify(texts),
      rubric_id: rubric_id,
      course_id: course_id,
      duration: duration,
      groupSize: groupSize,
      textOrImage: textOrImage,
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
    error: function(jqXHR, exception) {
      $('#id_error').text('Error');
    },
  });
  return false;
});

Dropzone.options.myAwesomeDropzone = {
  init: function() {
    this.on('success', function(file, response) {
      if (response.success === 1) {
        filePath = [...filePath, response.data.url];
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
        $(location).attr('href', '/activity');
      } else if (data.success === -99) {
        clearLoginCookie();
      } else {
        alert(data.message);
        $(location).attr('href', '/activity');
      }
    },
  });
}

$(document).ready(function() {
  $('input[type=radio][name=textOrImage]').change(function() {
    if (this.value == 'True') {
      // hide images form
      hide('my-awesome-dropzone');
      show('text-div');
      textOrImage = 'True';
    } else if (this.value == 'False') {
      // hide text inputs
      show('my-awesome-dropzone');
      hide('text-div');
      textOrImage = 'False';
    }
  });
});

function hide(id) {
  var element = document.getElementById(id);
  element.style.display = 'none';
  element.style.height = 0;
}

function show(id) {
  var element = document.getElementById(id);
  element.style.display = 'block';
  element.style.height = 'auto';
}
