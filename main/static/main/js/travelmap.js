var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        //zoom: 5,
        //center: new google.maps.LatLng(48.85,2.34),
        mapTypeId: 'terrain'
    });
    map.data.loadGeoJson($("#map").data('geojson'), [], function(features) {
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < features.length; i++) {
            if(features[i].getGeometry().getType() == 'Point') {
                a = features[i].getGeometry().get().lng();
                b = features[i].getGeometry().get().lat();
            } else if(features[i].getGeometry().getType() == 'LineString') {
                // Osef
            } else {
                console.error("Type inconnu : " + data.features[i].getGeometry().getType());
                continue;
            }
            point = new google.maps.LatLng(b, a);
            bounds.extend(point);
        }
        map.fitBounds(bounds);
    });
}
