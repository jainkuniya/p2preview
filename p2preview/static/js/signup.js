$("#signUpForm").submit(function () {
  $('#id_error').text('');

  var frm = $('#signUpForm');
  var email = $('#id_email').val();
  var password = $('#id_password').val();
  var name = $('#id_name').val();
  var office = $('#id_office').val();
  var department = $('#id_department').val();
  var visitingHours = $('#id_visitingHours').val();

  $.ajax({
    type: frm.attr('method'),
    url: '/api/v1/register/',
    data: {
      'email': email,
      'password': password,
      'name': name,
      'office': office,
      'department': department,
      'visitingHours': visitingHours,
      'personType': 1
    },
    dataType: 'json',
    success: function (data) {
      if (data.success === 1) {
        $('#id_success').text("Succesfully Registered");
        $(location).attr('href', '/')
      }else {
        $('#id_error').text(data.message);
      }
    }
  });
  return false;

});
