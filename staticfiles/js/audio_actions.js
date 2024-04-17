function increasePlayCount(trackId) {
    $.ajax({
        url: '/increase_play_count/' + trackId + '/',
        method: 'POST',
        success: function(data) {
            console.log(data.message);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}