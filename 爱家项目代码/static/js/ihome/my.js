function logout() {
    $.get("/api/logout", function (data) {
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function () {
    $.getJSON('/user/profile_info/', function (data) {
        console.log(data);
        $('#user-name').text(data.data.name);
        $('#user-mobile').text(data.data.phone);
        $('#user-avatar').attr('src', '/static/' + data.data.avatar)
    });

    $('#logout').click(function () {
        $.get('/user/logout/', function (data) {
            if (data.code == '200') {
                location.href = '/user/login/'
            }
        })
    });

});

