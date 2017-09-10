$("#signInForm").submit(function () {
  $('#id_error').text('');

  var frm = $('#signInForm');
  var email = $('#id_email').val();
  var password = $('#id_password').val();

  $.ajax({
    type: frm.attr('method'),
    url: '/api/v1/login/',
    data: {
      'email': email,
      'password': password
    },
    dataType: 'json',
    success: function (data) {
      if (data.success === 1) {
        document.cookie = "token=" +  data.token + "; path=/";
        $(location).attr('href', '/')
      }else {
        $('#id_error').text(data.message);
      }
    }
  });
  return false;

});
