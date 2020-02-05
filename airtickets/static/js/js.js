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

$(document).click(function (event) {
    console.log(event.target);
});

$('.results-list').on('click', '.result-item', function (event) {
    console.log(event.target.tagName != 'IMG');
    console.log(event.target.tagName);
    if (!event.target.tagName != 'IMG') {
        let departure_id = $(this).data('departure_id');
        let aircompany_id = $(this).data('aircompany_id');

        console.log(departure_id);


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
                'departure_id': departure_id,
                'aircompany_id': aircompany_id
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
    }


});


$('body').on('click', '.rating_icon', function () {
    console.log('rating ');
    let aircompany_id = $(this).data('aircompany_id');
    let rating = null;

    console.log($(this).hasClass('rating_up'));

    if ($(this).hasClass('rating_up')) {
        rating = 'up';
    } else if ($(this).hasClass('rating_down')) {
        rating = 'down'
    }

    console.log(rating);
    console.log(aircompany_id);


    $.ajax({
        url: 'ajax/aircompany_rating',
        data: {
            'aircompany_id': aircompany_id,
            'rating': rating
        },

        dataType: 'json',
        success: function (data) {
            alert(data.message);
        }
    })
});



let getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};

$(document).ready(function () {
    console.log("Started parsing...");
    from = getUrlParameter('from');
    to = getUrlParameter('to');
    date_from = getUrlParameter('date_from');
    date_to = getUrlParameter('date_to');


    if (from && to && date_from && date_to) {
        console.log('ajax request');

        $('.results-list').html(`
        <div class="loader">
            <div class="bar"></div>
        </div>
        `);

        $.ajax({
            url: '/ajax/departures_scrapper',
            data: {
                'from': from,
                'to': to,
                'date_from': date_from,
                'date_to': date_to
            },
            dataType: 'json',
            success: function (data) {
                $('.results-list').html("");
                for (let departure of data.departures) {
                    el = $(`
                        <a href="#">
                            <div class="result-item" data-departure_id ="${departure.departure_id}" data-aircompany_id="${departure.aircompany_id}">
                                <div class="flight-info">
                                    <p class="h4">${departure.aircompany_name}
                                        <a href="#">
                                            <img src="/static/img/rep_plus.svg" class='rating_icon rating_up' data-aircompany_id="${departure.aircompany_id}" alt="">
                                        </a>
                                        <a href="#">
                                            <img src="/static/img/rep_down.svg" class='rating_icon rating_down' data-aircompany_id="${departure.aircompany_id}" alt="">
                                        </a>
                                    </p>
                                    <div class="flight-info-item">
                                        <p class="h3">${departure.departure_time}</p>
                                        <p class="h5 disabled-text">${departure.departure_point_name}</p>
                                        <p class="h5 disabled-text">${departure.departure_date}</p>
                                        <p class="h5 disabled-text">${departure.name} - ${departure.plane}</p>
                                        <p class="h5 disabled-text">${departure.aircomany_rating} отзывов</p>
                                    </div>
                                    <div class="flight-info-item right-item">
                                        <p class="h3">${departure.arrival_time}</p>
                                        <p class="h5 disabled-text">${departure.arrival_point_name}</p>
                                        <p class="h5 disabled-text">${departure.arrival_date}</p>
                                    </div>
                                </div>
                            </div>
                        </a>
                    `);
                    $('.results-list').append(el);
                }
            },
            error: function (request, status, error) {
                alert(request.responseText, status)
            }
        })
    }
});
