window.onload = () => {
    //add event listener to prevent the default behavior
    const inputFields = document.querySelectorAll('input[type = number]');
    for (i = 0; i < inputFields.length; i++) {
        inputFields[i].addEventListener("keypress", (event) => {
            event.preventDefault();
          });
    }
  }

function send_order(clicked_id)
{
    var id = clicked_id.match(/\d+$/)[0];
    var amount = $("#amount_input" + id).val();
    var data = {"product_id" : id, "amount" : amount};
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/order',
        dataType : 'json',
        data : JSON.stringify(data)
    });
}