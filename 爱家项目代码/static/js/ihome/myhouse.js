$(document).ready(function () {
    $(".auth-warn").show();
});

$.getJSON('/user/auth_info/', function (data) {
    if (data.code == '200') {
        if (data.msg.id_name) {
            $('.auth-warn').hide();
            $('#houses-list').show()
        } else {
            $('.auth-warn').show();
            $('#houses-list').hide()
        }
    }
});

$(document).ready(function () {
    $.getJSON('/house/house_info/', function (data) {
        var house_info = '';
        for (var i = 0; i < data.data.length; i++) {
            console.log(data.data[i].title);
            house_info += '<li><a href="/house/detail/?house_id=' + data.data[i].id + '"> <div class="house-title"> <h3>房屋ID:' + data.data[i].id + ' —— ' + data.data[i].title + '</h3> </div> <div class="house-content"> <img src="/static/' + data.data[i].image + '" alt=""> <div class="house-text"> <ul> <li>' + data.data[i].area + '</li> <li>价格：￥' + data.data[i].price + '/晚</li> <li>发布时间：' + data.data[i].create_time + '</li> </ul> </div> </div> </a> </li>';
        }

        $('#houses-list').append(house_info);
    });
});