var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: new google.maps.LatLng(48.85,2.34),
        mapTypeId: 'terrain'
    });
    map.data.loadGeoJson('/train/stations.geojson', null, function(features) {
        var markers = features.map(function (feature) {
            var g = feature.getGeometry();
            var marker = new google.maps.Marker({ 'position': g.get(0) });
            return marker;
        });
        var clusterer = new MarkerClusterer(map, markers, {imagePath: '/static/main/img/m'});
    });
    map.data.setStyle(function (feature) {
        return { icon: feature.getProperty('icon'), visible: false };
    });
}
