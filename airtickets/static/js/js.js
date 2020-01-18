// if ($("#from").val().split(' ')[0] === $('#to').val().split(' ')[0])
$('#search-btn').click(function (event) {
    let from = ($("#from").val().split(' ')[0] == 'Международный') ? $("#from").val().split(' ')[$("#from").val().split(' ').length - 1] : $("#from").val().split(' ')[0];
    let to = ($("#to").val().split(' ')[0] == 'Международный') ? $("#to").val().split(' ')[$("#to").val().split(' ').length - 1] : $("#to").val().split(' ')[0];
    if (from === to) { // проверка места вылета
        event.preventDefault();
        $('#alert-box').html(`<div class="alert alert-danger" role="alert">
                                       Невозможно найти билеты в одном городе
                                 </div>`)
    } else if (new Date($("#date_from").val()).getTime() < new Date(new Date().toISOString().slice(0, 10)).getTime() ||
        new Date($("#date_from").val()).getTime() > new Date($("#date_to").val()).getTime()) { // проверка дат вылета
        event.preventDefault();
        $('#alert-box').html(`<div class="alert alert-danger" role="alert">
                                       Пожалуйста проверьте дату вылета.
                                 </div>`)
    } else {
        $('#alert-box').hide(500)
    }
});


$(window).scroll(function () { // изменение размеров хеадера
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
