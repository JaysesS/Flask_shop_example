window.onload = () => {
    const inputFields = document.querySelectorAll('input[type = number]');
    for (i = 0; i < inputFields.length; i++) {
        inputFields[i].addEventListener("keypress", (event) => {
            event.preventDefault();
          });
        inputFields[i].addEventListener("change", (event) => {
            var value = event.target.value;
            var id = (event.target.id).match(/\d+$/)[0];
            update_cost(id, value)
          });
    }
  }


function update_cost(id, value)
{
    data = {"id" : id, "amount" : value}
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/api/update_cost',
        dataType : 'json',
        data : JSON.stringify(data),
        success: function(res) {
            $("#user_cost").html("<h3>Total cost: <strong>$" + res['cost'] + "</strong></h3>");
        }
    });
}

function update_cost_all(){
    $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/get_cost',
        dataType : 'json',
        success: function(res) {
            $("#user_cost").html("<h3>Total cost: <strong>$" + res['cost'] + "</strong></h3>");
        }
    });
}

function checkCountInCart(){
    var count = $("#products div").length;
    console.log(count);
    if (count === 0){
        document.location.reload(true);
    }
}

function removeItemCart(id){
    var item_id = id.match(/\d+$/)[0];
    var data = {"id": item_id}
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/api/remove_item_cart',
        dataType : 'json',
        data : JSON.stringify(data),
        success: function(res) {
            $("#product" + item_id ).remove();
            update_cost_all();
            checkCountInCart();
        }
    });
}

function makeOrder()
{
    if (confirm('Did you check the data you entered in your account?')) {
        var divProducts = document.getElementById('products')
        var data = divProducts.querySelectorAll('input');
        var order = [];
        for (i = 0; i < data.length; i++) {
            var id = (data[i].id).match(/\d+$/)[0];
            var amount = data[i].value
            order.push({
                id: id,
                amount: amount
            })
        }
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/api/make_order',
            dataType : 'json',
            data : JSON.stringify(order),
            success: function(res) {
                $( ".info" ).empty();
                if (res["order"]){
                    $(".info").append("<div id = 'added_info' class='alert alert-success'><h3>"+ res["info"] +"</h3></div>");
                } else {
                    $(".info").append("<div id = 'added_info' class='alert alert-danger'><h3>"+ res["info"] +"</h3></div>");
                }
            }
        });
    }
}