const user_input = $("#user-input")
const search_icon = $('#search-icon')
const artists_div = $('#replaceable-content')
const endpoint = '/users/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            artists_div.fadeTo('slow', 0).promise().then(() => {
                // replace the HTML contents
                artists_div.html(response['html_from_view'])
                // fade-in the div with new contents
                artists_div.fadeTo('slow', 1)
                // stop animating search icon
                search_icon.removeClass('blink')
            })
        })
}


user_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }

    // start animating the search icon with the CSS class
    search_icon.addClass('blink')

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})




$(".dropdown-menu li a").click(function(e){
    e.preventDefault()
    var selText = $(this).text();
    $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});


function getValue(){
  var selected = document.getElementById("id_TaskId");
  var selectedText = selected.options[selected.selectedIndex].text;
}
function goBack() {
  window.history.back();
}

$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
