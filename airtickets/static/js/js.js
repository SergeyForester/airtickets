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

$(".result-item").click(function () {
    let flightId = $(this).data('flight_id');
    let aircomapany_id = $(this).data('aircomapany_id');

    console.log(flightId);


    $(".results-list").addClass('results-inline');
    $(".result-item").addClass('result-item-details');
    $("#result-info").addClass('result-info-details-inline');
    $('.result-item').addClass('result-item-ajax');

    $(".result-info-details").html(`
        <img src="/static/img/preloader.gif"></img>
    `);

    $.ajax({
        url: '/ajax/flight_info',
        data: {
            'flight_id': flightId,
            'aircomapany_id': aircomapany_id
        },
        dataType: 'json',
        success: function (data) {

            if (data) {
                $("#result-info").html(`
              <div class="result-info-wrapper">
                <div class="result-info-details">
                    <div class="result-info-header">
                      <p class="h5">${data.aircompany} - ${data.aircompany_rating}</p>
                    </div>
                    <p class="h4 disabled-text">Рейс ${data.flight_code} </p>
                     <p class="h3">Из ${data.from} в ${data.to}</p> 
                     <p class="h4">Время вылета ${new Date(data.date_from).toISOString()}, время прилета ${new Date(data.date_to).toISOString()}</p>
                     <div class="result-info-aircompany_description">
                         <p class="h5">
                            ${data.aircompany_description}
                         </p>
                     </div>
                     <div class="empty-space"></div>
                </div>
              </div>`);
            }
        }
    });

});


