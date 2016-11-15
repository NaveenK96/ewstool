var data = [];
var otherdata = [];

function initData(input, input2) {
    data = input;
    otherdata = input2;
    console.log(otherdata);
}

var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.111674, lng: -88.227017},
        zoom: 17,
        mapTypeControl: false,
        scaleControl: true,
        disableDoubleClickZoom: true,
        scrollwheel: false
    });
    data.map(function(item) {
        var fillColor = "00FF00"
        var pinImage = new google.maps.MarkerImage("https://chart.apis.google.com/chart?chst=d_map_spin&chld=.8|0|" + fillColor + "|9|_|" + item.name);
        var marker = new google.maps.Marker({
            position: {lat: item.lat, lng: item.lng},
            map: map,
            title: item.name,
            icon:pinImage
        });
        var contentString = '<h1>Labs</h1>';
        var infowindow = new google.maps.InfoWindow({
          content: contentString
        });
        marker.addListener('mouseover', function() {
          infowindow.open(map, marker);
        });
        marker.addListener('mouseout', function() {
          infowindow.close(map, marker);
        });
    });
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        map.setCenter(pos);
        }, function() {
            // handleLocationError(true, infoWindow, map.getCenter());
            // alert("Geolocation not supported.");
        });
    } else {
        // Browser doesn't support Geolocation
        // handleLocationError(false, infoWindow, map.getCenter());
        // alert("Geolocation not supported.");
    }
    if (typeof(Storage) !== "undefined") {
        var favorites = localStorage.getItem("favorites");
        $.post("/", {
                favorites: favorites
            },
            function (data, status) {
                if (status == 'success') {
                    $('#accordion').append(data.html);
                    $('.fa.fa-star-o').click(handlero);
                    $('.fa.fa-star').click(handler);
                    $('.panel-body').click(handler_panel);
                }
            }
        );
    }
}

$(function () {
    var $menu = $('#sidebar-wrapper');
    var $content = $('#main-wrapper');
    $content.addClass('no-transition');
    $menu.hide();
    $menu.css('left', -($menu.outerWidth() + 10));
    $content.removeClass('col-md-9').addClass('col-md-12');
    $('#toggle-button').click(function () {
        $content.removeClass('no-transition');
        if ($menu.is(':visible') && $content.hasClass('col-md-9')) {
            // Slide out
            $menu.animate({
                left: -($menu.outerWidth() + 10)
            }, function () {
                $menu.hide(1000);
            });
            $content.removeClass('col-md-9').addClass('col-md-12');
        }
        else {
            // Slide in
            $menu.show(0).animate({ left: 0 });
            $content.removeClass('col-md-12').addClass('col-md-9');
        }
        if($content.hasClass('col-md-12') && $menu.is(':hidden')) {
        $menu.animate({
                left: 0
            }, function () {
                $menu.show(0);
            });
        //  $menu.show();
        $content.removeClass('no-transition');
        $content.removeClass('col-md-12').addClass('col-md-9');
        }
    });
    $('#current-location').click(function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
            }, function() {
                map.setCenter({lat: 40.111674, lng: -88.227017});
                // alert("Geolocation not supported.");
            });
        } else {
            map.setCenter({lat: 40.111674, lng: -88.227017});
            // alert("Geolocation not supported.");
        }
    });
});

function handlero() {
    var data = $(this).parent().children($('.hidden')).text().split(",");
    var favorites = localStorage.getItem("favorites");
    $.post("/", {
            favorites: favorites,
            building: data[2],
            lab: data[3],
            option: "ADD"
        },
        function (data, status) {
            if (status == 'success') {
                $('#accordion').empty();
                $('#accordion').append(data.html);
                $('.fa.fa-star-o').click(handlero);
                $('.fa.fa-star').click(handler);
                $('.panel-body').click(handler_panel);
                localStorage.setItem("favorites", JSON.stringify(data.favorites));
            }
        }
    );
}

function handler() {
    var data = $(this).parent().children($('.hidden')).text().split(",");
    var favorites = localStorage.getItem("favorites");
    $.post("/", {
            favorites: favorites,
            building: data[2],
            lab: data[3],
            option: "REMOVE"
        },
        function (data, status) {
            if (status == 'success') {
                $('#accordion').empty();
                $('#accordion').append(data.html);
                $('.fa.fa-star-o').click(handlero);
                $('.fa.fa-star').click(handler);
                $('.panel-body').click(handler_panel);
                localStorage.setItem("favorites", JSON.stringify(data.favorites));
            }
        }
    );
}

function handler_panel() {
    var coords = $(this).find("div").text().split(",");
    map.setCenter({'lat':parseFloat(coords[0]), 'lng':parseFloat(coords[1])})
}
