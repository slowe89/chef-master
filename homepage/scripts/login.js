$(function(){

    $('#login_form').ajaxForm(function(data){
        $('#jquery-loadmodal-js-body').html(data);
    });//login form

}); //end
