alert(`Important Instructions:
1. This is a sample app with functional bugs, and you have 45 minutes of time to uncover all the the bugs. 
2. To understand the product: https://www.youtube.com/watch?v=JmY7h8w4wEo
3. Time starts as soon as you login so make sure you keep all your required things for testing and noting down the bugs like screenshot taker, notepad, pen paper etc.
4. Do NOT logout until you plan to, because you won’t be allowed to take the test again.
5. After the test, share the bugs or observations you had with the application.`);

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
