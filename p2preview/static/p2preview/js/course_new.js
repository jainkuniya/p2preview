$.getScript('/static/p2preview/js/commonJs.js', function() {
  // script is now loaded and executed.
  // put your dependent JS here.

  $('#newCourseForm').submit(function() {
    $('#id_error').text('');

    var frm = $('#newCourseForm');
    var name = $('#id_course_name').val();
    var description = $('#id_course_description').val();

    $.ajax({
      type: frm.attr('method'),
      beforeSend: function(request) {
        request.setRequestHeader('TOKEN', getCookie('token'));
      },
      url: '/api/v1/create_course/',
      data: {
        name: name,
        description: description
      },
      dataType: 'json',
      success: function(data) {
        if (data.success === 1) {
           $(location).attr('href', '/course');
        } else if(data.success === -99){
          clearLoginCookie();
        }
        else {
          $('#id_error').text(data.message);
        }
      }
    });
    return false;
  });
});
