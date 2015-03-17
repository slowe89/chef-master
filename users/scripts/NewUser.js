$(function() {

    $('#id_username').on('change', function () {

        var username = $(this).val();

        $.ajax({
            url: '/users/users.check_username/',
            type: 'POST',
            data: {
                'username': username
            },
            success: function (resp) {

                if (resp == 'available') {
                    $('#id_username').parent().removeAttr('isInvalid').removeAttr('error');
                }
                else {
                    $('#id_username').parent().attr('isInvalid', 'True').attr('error', 'This username is already taken');
                }

            }
        });
    });
});
