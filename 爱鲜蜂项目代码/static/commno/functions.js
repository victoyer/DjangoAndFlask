function addCart(goods_id) {
    // $.get('axf/addCart/?goods_id=' + goods_id, function (msg) {
    //
    //     if (msg.code == 200){
    //         $('#num_' + goods_id)
    //     }else{
    //
    //     }
    // });
    var csrf = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: '/axf/addCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.code == 200) {
                $('#num_' + goods_id).text(msg.c_num)
            } else {
                alert(msg.msg)
            }
        },
        error: function () {
            alert('请求失败')
        }
    })
}

function subCart(goods_id) {
    var csrf = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: '/axf/subCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == 200) {
                $('#num_' + goods_id).text(data.c_num)
            } else {
                alert(data.msg)
            }
        },
        error: function (data) {
            alert('请求失败')
        }
    });
}

//改变商品状态
function changeSelectStatus(cart_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/changeSelectStatus/',
        type: 'POST',
        dataType: 'json',
        data: {'cart_id': cart_id},
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == 200) {
                if (data.is_select) {
                    $('#cart_id_' + cart_id).text('√')
                } else {
                    $('#cart_id_' + cart_id).text('×')
                }
            }
        },
        error: function (data) {
            alert('请求失败')
        },
    });
}


//
// (function () {
//     $.ajax({
//         url: '/axf/infoCart/',
//         type: 'GET',
//         dataType: 'json',
//         success: function (msg) {
//             // alert(msg.goods_id);
//             alert(msg.c_num);
//             if (msg.code == 200) {
//                 for (var i = 1; i < msg.goods_id.length;)
//                 $('#num_')
//             }
//         },
//         error: function (msg) {
//             alert(msg.msg)
//         }
//
//     });
//
//
// }());

// function chioce(id) {
//     var csrf = $('input[name=csrfmiddlewaretoken]').val();
//     $.ajax({
//         url: '/axf/totalchoice/',
//         type: 'POST',
//         dataType: 'json',
//         data: {'id': id},
//         headers: {'X-CSRFToken': csrf},
//         success: function (data) {
//             if (data.code == 200) {
//
//             }
//         },
//         error: function (data) {
//             alert('请求失败')
//         }
//
//     })
// }


// function change_order(order_id) {
//     // alert(order_id)
//     var csrf = $('input[name=csrfmiddlewaretoken]').val();
//     $.ajax({
//         url: '/axf/changeOrder/',
//         type: 'POST',
//         data: {'order_id': order_id},
//         dataType: 'json',
//         headers: {'X-CSRFToken': csrf},
//         success: function (data) {
//             if (data.code == 200) {
//                 location.href = '/axf/mine/'
//             }
//         },
//         error: function (data) {
//             alert('修改订单失败')
//         }
//     })
// }

