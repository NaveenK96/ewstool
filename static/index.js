$(function () {
    var $menu = $('#sidebar-wrapper');
    var $content = $('#main-wrapper');
    $content.addClass('no-transition');
    $menu.hide();
    $menu.css('left', -($menu.outerWidth() + 10));
    $content.removeClass('col-md-10').addClass('col-md-12');
    $('#toggle-button').click(function () {
        $content.removeClass('no-transition');
        if ($menu.is(':visible') && $content.hasClass('col-md-10')) {
            // Slide out
            $menu.animate({
                left: -($menu.outerWidth() + 10)
            }, function () {
                $menu.hide(1000);
            });
            $content.removeClass('col-md-10').addClass('col-md-12');
        }
        else {
            // Slide in
            $menu.show(500).animate({ left: 0 });
            $content.removeClass('col-md-12').addClass('col-md-10');
        }
        if($content.hasClass('col-md-12') && $menu.is(':hidden')) {
        $menu.animate({
                left: 0
            }, function () {
                $menu.show(1000);
            });
        //  $menu.show();
        $content.removeClass('no-transition');
        $content.removeClass('col-md-12').addClass('col-md-10');
        }
    });
});
