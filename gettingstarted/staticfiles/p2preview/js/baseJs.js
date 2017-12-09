function logout() {
  $.ajax({
    url: '/api/v1/logout/', //the page containing php script
    type: 'GET', //request type
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', getCookie('token'));
    },
    success: function(result) {
      clearLoginCookie();
    }
  });
}

$(document).ready(function() {
 
   fetchSelf();
});

function fetchSelf() {
  var token = getCookie('token');
  if (token !== '')
  { $.ajax({
    url: '/api/v1/fetch_self/', //the page containing php script
    type: 'GET', //request type
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', token);
    },
    success: function(result) {
      if (result.success === 1)
      {
        $("#dropdownMenuLink").text("Hi, " + result.self.name + "!");
        $("#login").addClass("hideItem");
        $("#signUp").addClass("hideItem");
      }else
      {
        clearLoginCookie();
      }
      
    }
  });
  }
  else
  {
    $("#editProfile").addClass("hideItem");
    $("#logout").addClass("hideItem");
  }
}
