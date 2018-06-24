function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {

    $('#form-avatar').submit(function () {

        $(this).ajaxSubmit({
            url: '/user/profile_img/',
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.code == '200') {
                    $('#user-avatar').attr('src', '/static/' + data.msg)
                }
                if (data.code != '200') {
                    $('.error-msg').text(data.msg);
                    $('.error-msg').show()
                }
            },
            error: function (data) {
                alert('请求失败！')
            }
        });
        return false;
    });


    $('#form-name').submit(function () {
        // console.log($('#user-name').val());
        $.ajax({
            url: '/user/profile_name/',
            type: 'POST',
            data: {'name': $('#user-name').val()},
            dataType: 'json',
            success: function (data) {
                if (data.code == '200') {
                    $('#user-name').attr('placeholder', data.msg)
                }
                if (data.code != '200') {
                    $('.error-msg').text(data.msg);
                    $('.error-msg').show()
                }


            },
            error: function (data) {
                alert('请求失败！')
            }
        });
        return false;
    });

});

$('#user-name').blur(function () {

    $.ajax({
        url: '/user/profile_name/',
        type: 'POST',
        dataType: 'json',
        data: {'name': $('#user-name').val()},
        success: function (data) {
            if (data.code == '200') {

                $('.error-msg').hide()
            }
            if (data.code != '200') {
                $('.error-msg').text(data.msg);
                $('.error-msg').show()
            }

        },
        error: function (data) {
            alert('请求失败')
        }
    });

});


(function () {

    $.ajax({
        url: '/user/profile_info/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#user-avatar').attr('src', '/static/' + data.data.avatar);
            $('#user-name').attr('placeholder', data.data.name)
        },
        error: function (data) {
            alert('请求失败！')
        }
    });


}());
