$('#search-btn').click(function (event) {
    if ($("#from").val().split(' ')[0] === $('#to').val().split(' ')[0]) {
        event.preventDefault();
        $('#alert-box').html(`<div class="alert alert-danger" role="alert">
                                       Невозможно найти билеты в одном городе
                                 </div>`)
    } else {
        $('#alert-box').hide(500)
    }
});


$(window).scroll(function () {
    if ($(window).width() > 481) {
        if ($(this).scrollTop() > 100) {
            $('.search-header').height('10vh');
            $('#search-navbar').hide();
        } else {
            $('.search-header').height('20vh');
            $('#search-navbar').show(200);

        }
    }

});
