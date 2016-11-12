function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.111667, lng: -88.227017},
        zoom: 17,
        mapTypeControl: false,
        scaleControl: true,
        disableDoubleClickZoom: true
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
        });
    } else {
        // Browser doesn't support Geolocation
        // handleLocationError(false, infoWindow, map.getCenter());
    }
}
