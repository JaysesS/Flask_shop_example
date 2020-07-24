window.onload = () => {
    const inputFields = document.querySelectorAll('input[type = number]');
    for (i = 0; i < inputFields.length; i++) {
        inputFields[i].addEventListener("keypress", (event) => {
            event.preventDefault();
          });
    }
  }


function sendToCart(clicked_id)
{
    var id = clicked_id.match(/\d+$/)[0];
    var amount_id = "#amount_input" + id
    var amount = $(amount_id).val();
    var data = {"id" : id, "amount" : amount}
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/api/add_to_cart',
        dataType : 'json',
        data : JSON.stringify(data),
        success: function() {
            toggleAlert()
        }
    });
    $(amount_id).val("1");
}

function toggleAlert(){
    $(".alert").fadeTo(3000, 500).slideUp(500, function(){
        $("#success-alert").slideUp(500);
    });
    return false;
}

$('#alertToCart').on('close.bs.alert', toggleAlert)