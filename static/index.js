var map;
var url;
var buildings;

function init(data, input) {
    buildings = data;
    url = input;
}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.111674, lng: -88.227017},
        zoom: 17,
        mapTypeControl: false,
        scaleControl: true,
        disableDoubleClickZoom: true,
        scrollwheel: false
    });
    Object.keys(buildings).map(function(building) {
        var fillColors = ["00FF00", "33FF00", "66FF00", "99FF00", "CCFF00", "FFFF00", "FFCC00", "FF9900", "FF6600", "FF3300", "FF0000"];
        var index = Math.ceil(((buildings[building].inuse / buildings[building].total) * fillColors.length) - 1);
        index = index == -1 ? 0 : index;
        var fillColor = fillColors[index];
        var pinImage = new google.maps.MarkerImage("https://chart.apis.google.com/chart?chst=d_map_spin&chld=.8|0|" + fillColor + "|9|_|" + building);
        var marker = new google.maps.Marker({
            position: {lat: buildings[building].latitude, lng: buildings[building].longitude},
            map: map,
            title: buildings[building].long_name,
            icon: pinImage
        });
        var contentString = '<div class="text-center"><h4>' + buildings[building].long_name + '<br><small>' + buildings[building].address +  '</small></h4><p></p>' + buildings[building].hours + '<h5>In use: <small>' + buildings[building].inuse.toString() + ' / ' + buildings[building].total.toString() + '</small></h5></div>';
        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });
        marker.addListener('mouseover', function() {
            infowindow.open(map, marker);
        });
        marker.addListener('mouseout', function() {
            infowindow.close(map, marker);
        });
        marker.addListener('click', function() {
            window.location.replace(url + "/" + building);
        });
    });
    var controlDiv = document.createElement('div');
    var controlUI = document.createElement('div');
    controlUI.style.boxShadow = 'rgba(0, 0, 0, 0.298039) 0px 1px 4px -1px';
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.marginBottom = '32px';
    controlUI.style.textAlign = 'center';
    controlDiv.appendChild(controlUI);
    var controlText = document.createElement('div');
    controlText.style.fontFamily = '"Times New Roman", Times, serif';
    controlText.style.fontSize = '16px';
    controlText.style.padding = '8px';
    controlText.textContent = 'Green: Empty -> Red: Full';
    controlUI.appendChild(controlText);
    map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(controlDiv);
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
}

$(function () {
    $('.fa.fa-star-o').click(handler_favorite);
    $('.fa.fa-star').click(handler_unfavorite);
    $('.panel-body').click(handler_panel);

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
                alert("Geolocation not supported.");
            });
        } else {
            alert("Geolocation not supported.");
        }
    });
    if (typeof(Storage) !== "undefined") {
        var favorites = JSON.parse(localStorage.getItem("favorites"));
        if (favorites != null) {
            if (favorites.length != 0) {
                $(".panel.panel-info").show()
            }
            for (var i = 0; i < favorites.length; i++) {
                var name = "#favorite-" + favorites[i];
                $(name).show();
                name = "#" + favorites[i];
                $(name).hide();
            }
        }
    }
});
function handler_favorite() {
    if (typeof(Storage) !== "undefined") {
        $(".panel.panel-info").show()
        var id = $(this).parent().parent().parent().attr('id');
        var favorites = JSON.parse(localStorage.getItem("favorites"));
        favorites.push(id);
        localStorage.setItem("favorites", JSON.stringify(favorites));
        var name = "#favorite-" + id;
        $(name).show();
        name = "#" + id;
        $(name).hide();
    }
}
function handler_unfavorite() {
    if (typeof(Storage) !== "undefined") {
        var id = $(this).parent().parent().parent().attr('id').split('-')[1];
        var favorites = JSON.parse(localStorage.getItem("favorites"));
        var index = favorites.indexOf(id);
        if (index > -1) {
            favorites.splice(index, 1);
        }
        localStorage.setItem("favorites", JSON.stringify(favorites));
        if (favorites.length == 0) {
            $(".panel.panel-info").hide()
        }
        var name = "#favorite-" + id;
        $(name).hide();
        name = "#" + id;
        $(name).show();
    }
}

function handler_panel() {
    var id = $(this).attr('id').split("-");
    if (id.length == 2) {
        id = id[1];
    } else {
        id = id[0].replace('#', '');
    }
    var pos;
    var keys = Object.keys(buildings);
    for (var i = 0; i < keys.length; i++) {
        if (id in buildings[keys[i]].labs) {
            pos = {'lat': buildings[keys[i]].latitude, 'lng': buildings[keys[i]].longitude};
        }
    }
    map.setCenter(pos)
}
