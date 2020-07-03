window.onload = () => {
    const inputFields = document.querySelectorAll('input[type = number]');
    for (i = 0; i < inputFields.length; i++) {
        inputFields[i].addEventListener("keypress", (event) => {
            event.preventDefault();
          });
    }
  }


function sendOrder(clicked_id)
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
        data : JSON.stringify(data)
    });
    $(amount_id).val("1");
}