function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // 房屋信息
    $.ajax({
        url: '/house/area_facility/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {

            // 所在区域
            // console.log(data.msg);
            totle = '';
            for (var i = 0; i < data.msg.length; i++) {
                totle += '<option value="' + data.msg[i].id + '">' + data.msg[i].name + '</option>'
            }
            $('#area-id').html(totle);

            // 房间设施
            // console.log(data.data);
            whole = '';
            for (var i = 0; i < data.data.length; i++) {
                // alert('<li> <div class="checkbox"> <label> <input type="checkbox" name="facility" value="' + data.data[i].id + '">' + data.data[i].name + '</label> </div> </li>');
                whole += '<li> <div class="checkbox"> <label> <input type="checkbox" name="facility" value="' + data.data[i].id + '">' + data.data[i].name + '</label> </div> </li>'
            }
            $('.clearfix').html(whole);

        },
        error: function (data) {
            alert('请求失败！')
        }
    });

    // 房源信息提交
    $('#form-house-info').submit(function () {

        $.post('/house/newhouse/', $(this).serialize(), function (data) {
            if (data.code == '200') {
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(data.house_id);
            }
        });
        return false;
    });

    $('#form-house-image').submit(function () {
        $(this).ajaxSubmit({
            url: '/house/house_image/',
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                // console.log(data);
                if (data.code == '200') {
                    $('.house-image-cons').append('<img src="/static/' + data.img + '">')
                }
            },
            error: function (data) {
                alert('请求失败')
            }
        });
        return false;
    })


});

