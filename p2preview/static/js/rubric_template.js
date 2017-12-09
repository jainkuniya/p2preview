$('#allCriteriaList').submit(function() {
  var frm = $('#newCriteriaForm');
  var rubric_name = $('#id_rubric_name').val();

  var values3 = {};
  $.each($('#allCriteriaList').serializeArray(), function(i, field) {
    values3[field.name] = field.value;
  });

  $.ajax({
    type: 'post',
    beforeSend: function(request) {
      request.setRequestHeader('TOKEN', getCookie('token'));
    },
    url: '/api/v1/create_rubric/',
    data: {
      rubric_name: rubric_name,
      criterias: JSON.stringify(values3),
    },
    dataType: 'json',
    success: function(data) {
      if (data.success === 1) {
        $(location).attr('href', '/rubricTemplate');
      } else if (data.success === -99) {
        clearLoginCookie();
      } else {
        $('#id_error').text(data.message);
      }
    },
  });
  return false;
});

// get selected checkboxes
function getSelectedChbox(frm) {
  var selchbox = []; // array that will store the value of selected checkboxes
  // gets all the input tags in frm, and their number
  var inpfields = frm.getElementsByTagName('selectedStatus');
  var nr_inpfields = inpfields.length;
  // traverse the inpfields elements, and adds the value of selected (checked) checkbox in selchbox
  for (var i = 0; i < nr_inpfields; i++) {
    if (inpfields[i].type == 'checkbox' && inpfields[i].checked == true)
      selchbox.push(inpfields[i].value);
  }
  alert(selchbox);
  return selchbox;
}
