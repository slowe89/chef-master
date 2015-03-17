
$(function(){

    $('.btn-danger').click( function(){

        var id = $(this).attr('data-id');

        $.ajax({

            url: "/inventory/shopping_cart.delete/" + id

        }).done(function(data) {
            $('#cart').find('.modal-body').html(data)
        })

    });

});