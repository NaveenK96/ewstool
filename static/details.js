var buildings;

function init(data) {
    buildings = data;
}
$(function () {
    $('.active').click(handler);
    $('.off').click(handler);
});
function handler() {
    var id = $(this).attr('id').split("-")[1];
    var old_id = $('.active').attr('id').split("-")[1];
    $('#button-' + old_id).removeClass('active').addClass('off');
    $(this).removeClass('off').addClass('active');
    $('#detail-' + old_id).hide();
    $('#detail-' + id).show();
}
