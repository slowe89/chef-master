$(function(){

    $('#show_login').click(function(){

        $.loadmodal({
            url: '/homepage/login/',
            width: 600,
            title: 'Login'
        })

    }); //click event

    $('#change_password').click(function(){

        $.loadmodal({
            url: '/users/users.edit_my_password/',
            width: 600,
            title: 'Change Password',
            id: 'password_modal'
        })

    }); //click event

    $('#view_cart').click(function(){

        $.loadmodal({
            url: '/inventory/shopping_cart/',
            width: 600,
            title: 'Shopping Cart',
            id: 'my_cart'
        })

    }); //click event

    $('#cart_button').on('click', function(){

    var item = $(this).attr('data-pid');
    var qty = $('#qty').val();

    $.loadmodal({

        url: "/inventory/shopping_cart.add/" + item + "/" + qty,
        title: 'Shopping Cart',
        width:'600px',
        id: 'cart'

        })

    }); //click event

    $('#search').on('click', function(){

    $.loadmodal({

        url: "/inventory/products.find/",
        title: 'Find:',
        width:'400px',
        id: 'find'

        })

    }); //click event

});//end