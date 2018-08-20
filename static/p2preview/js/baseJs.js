var loginTime = 0;
var allowedTimeInMin = 0;

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

async function checkForTimeLeft() {
  var t = Date.now() - loginTime;
  
  if (t > allowedTimeInMin * 60 * 1000) {
    alert('Thank you for your time, please revert to the mail along with the bugs you found with your observations in your prefered way. Our team will evaluate and get to you max within 2 days.');
    logout();
    return;
  }

  var timeRemaining =  (allowedTimeInMin * 60 * 1000 - t)/1000;

  $('#timeleft').text('Time left: ' + parseInt(timeRemaining / 60) + ' mins ' + parseInt(timeRemaining % 60) + ' secs ');
  setTimeout(checkForTimeLeft, 1000);
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
          loginTime = result.self.login_time;
          allowedTimeInMin = result.self.task_time_in_min;
          checkForTimeLeft();
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
