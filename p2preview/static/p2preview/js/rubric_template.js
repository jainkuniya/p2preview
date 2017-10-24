$('#submitButton').click(function() {
  $('#id_error').text('');
  var frm = $('#newCriteriaForm');
  var description = $('#id_description').val();
  var option1 = $('#option1').val();
  var option2 = $('#option2').val();
  var option3 = $('#option3').val();
  var option4 = $('#option4').val();
  var option1Points = $('#option1Points').val();
  var option2Points = $('#option2Points').val();
  var option3Points = $('#option3Points').val();
  var option4Points = $('#option4Points').val();
  var answer = $('#answer').val();

  $.ajax({
    type: 'post',
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', getCookie('token'));
    },
    url: '/api/v1/create_generic/',
    data: {
      description: description,
      option1: option1,
      option2: option2,
      option3: option3,
      option4: option4,
      option1Points: option1Points,
      option2Points: option1Points,
      option3Points: option1Points,
      option4Points: option1Points,
      answer: answer,
    },
    dataType: 'json',
    success: function(data) {
      alert(data);
      if (data.success === 1) {
        //$(location).attr('href', '/course');
      } else if (data.success === -99) {
        clearLoginCookie();
      } else {
        $('#id_error').text(data.message);
      }
    },
  });
  return false;
});
