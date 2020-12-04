$(function () {
    $('#startbutton').click(function () {
        var userID = $(this).attr('name')
        var reportID = $(this).attr('report')
        $.ajax({
            url: 'record/',
            method: 'POST',
            data: {
                name: 'start',
                click: true,
                question: 1,
                userID: userID,
                reportID: reportID
            },
            success: function (data) {
                if (response.result != 'success') {
                    console.error(response.data)
                    return;
                }
            }
        });
    });
});
$(function () {
    $('#finishbutton').click(function () {
        var userID = $(this).attr('name')
        $.ajax({
            url: 'record_stop/',
            method: 'POST',
            data: {
                name: 'finish',
                click: true,
                question: 1,
                userID: userID
            },
            success: function (data) {
                if (response.result != 'success') {
                    console.error(response.data)
                    return;
                }
            }
        });
    });
});