function logout() {
  $.ajax({
    url: '/api/v1/logout/', //the page containing php script
    type: 'GET', //request type
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', getCookie('token'));
    },
    success: function(result) {
      clearLoginCookie();
    },
  });
}

$(document).ready(function() {
  fetchSelf();
});

function checkForTimeLeft(loginTime, allowedTimeInMin) {
  var t = Date.now() - loginTime;
  if (t > allowedTimeInMin * 60) {
    alert('Time completed');
    logout();
    return;
  }
  $('#dropdownMenuLink').text('Time left:' + t / 60 + 'mins ' + (t % 60) + 'secs ');
  setTimeout(checkForTimeLeft(loginTime, allowedTimeInMin), 500);
}

function fetchSelf() {
  var token = getCookie('token');
  if (token !== '') {
    $.ajax({
      url: '/api/v1/fetch_self/', //the page containing php script
      type: 'GET', //request type
      beforeSend: function(request) {
        request.setRequestHeader('TOKEN', token);
      },
      success: function(result) {
        if (result.success === 1) {
          var loginTime = result.self.login_time;
          var allowedTimeInMin = result.self.task_time_in_min;
          checkForTimeLeft(loginTime, allowedTimeInMin);
          $('#dropdownMenuLink').text('Hi, ' + result.self.name + '!');
          $('#login').addClass('hideItem');
          $('#signUp').addClass('hideItem');
        } else {
          clearLoginCookie();
        }
      },
    });
  } else {
    $('#editProfile').addClass('hideItem');
    $('#logout').addClass('hideItem');
  }
}
