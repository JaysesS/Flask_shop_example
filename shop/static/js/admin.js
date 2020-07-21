function fill_all_products() {
    $.ajax({
        type: 'GET',
        url: '/api/fill_products',
        success: function(res) {
            console.log('fill')
        }
    });
}

function delete_all_products() {
    $.ajax({
        type: 'GET',
        url: '/api/delete_products',
        success: function(res) {
            console.log('delete')
        }
    });
}