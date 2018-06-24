function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {


    var path = location.search;
    var id = path.split('=')[1];

    $.get('/house/detail/' + id + '/', function (data) {
        console.log(data);
        $('.house-price').html('￥<span>' + data.msg.price + '</span>/晚');
        $('.house-title').text(data.msg.title);
        $('.landlord-name').html('房东： <span>' + data.msg.user_name + '</span>');
        $('.text-center').html('<li>' + data.msg.address + '</li>');
        $('#house_num').text('出租' + data.msg.room_count + '间');
        $('#house_acreage').text('房屋面积:' + data.msg.acreage + '平米');
        $('#house_unit').text('房屋户型:' + data.msg.unit + '');
        $('#house_capacity').text('宜住' + data.msg.capacity + '人');
        $('#house_beds').text(data.msg.beds);
        $('#house_deposit').text(data.msg.deposit);
        $('#house_min_days').text(data.msg.min_days);
        $('#house_max_days').text(data.msg.max_days);
        $('.landlord-pic').html('<img src="/static/' + data.msg.user_avatar + '">');
        $('.book-house').attr('href', '/house/booking/?house_id=' + data.msg.id);

        var html = '';
        for (var i = 0; i < data.msg.images.length; i++) {
            html += '<li class="swiper-slide"><img src="/static/' + data.msg.images[i] + '"></li>'
        }
        $('.swiper-wrapper').append(html);

        var total = '';
        for (var i = 0; i < data.msg.facilities.length; i++) {
            total += '<li><span class="' + data.msg.facilities[i].css + '"></span>' + data.msg.facilities[i].name + '</li>'
        }
        $('.house-facility-list').append(total);


        var mySwiper = new Swiper('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
        });
        $(".book-house").show();

    })


});