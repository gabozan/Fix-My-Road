$(document).ready(function() {
    $('#login-btn').mouseenter(function() {
        $('#user-menu').show();
    });

    $('.dropdown').mouseleave(function() {
        $('#user-menu').hide();
    });
});