
$(function(){

   $('#go_find').click( function(){
            var productName = $('#search_input').val();

            $.ajax({
                url: '/inventory/products.find',
                data:{
                    name: productName
                }
            }).done(function(data) {
                $('#find').modal('hide');
                window.location.replace(data);
                console.log(productName)
            })
    });

});