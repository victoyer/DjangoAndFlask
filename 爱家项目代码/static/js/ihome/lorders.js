//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {

    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    $('.modal-accept').click(function () {
        var order_id = $(this).attr('order-id');
        var status = 'WAIT_PAYMENT';

        $.ajax({
            url: '/order/accept_order/',
            type: 'PATCH',
            data: {'order_id': order_id, 'status': status},
            dataType: 'json',
            success: function (data) {
                location.href = '/order/lorders/'
            },
            error: function (data) {
                alert('请求失败')
            }
        });
        return false;
    });

    $('.modal-reject').click(function () {
        var order_id = $(this).attr('order-id');
        var status = 'REJECTED';
        var comment = $('#reject-reason').val();
        // console.log(comment);

        $.ajax({
            url: '/order/accept_order/',
            type: 'PATCH',
            data: {'order_id': order_id, 'status': status, 'comment': comment},
            dataType: 'json',
            success: function (data) {
                location.href = '/order/lorders/'
            },
            error: function (data) {
                alert('请求失败')
            }
        });
        return false;
    });


    $.get('/order/lordersinfo/', function (data) {
        var html = template('templates_infos', {orders: data.msg});
        $('.orders-list').html(html);


        $(".order-accept").on("click", function () {

            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
        });
        $(".order-reject").on("click", function () {
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-reject").attr("order-id", orderId);
        });


    });


});



