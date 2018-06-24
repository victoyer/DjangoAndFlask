function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    $('#form-auth').submit(function () {
        $.ajax({
            url: '/user/auth/',
            type: 'POST',
            dataType: 'json',
            data: {'iname': $('#real-name').val(), 'icard': $('#id-card').val()},
            success: function (data) {
                if (data.code == '200') {
                    $('.btn-success').hide()
                }
            },
            error: function (data) {
                alert('请求失败')
            }
        });
        return false;
    });
});

$.getJSON('/user/auth_info/', function (data) {
    if (data.code == '200') {

        if (data.msg.id_card) {
            $('#real-name').val(data.msg.id_name);
            $('#id-card').val(data.msg.id_card);
            $('.btn-success').hide()
        }
    }
});
