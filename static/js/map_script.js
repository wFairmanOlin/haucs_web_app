let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 40,
    center: { lat: 27.5293081, lng: -80.3512673},
    mapTypeId: 'satellite',
    tilt:0
  });
  // Load GeoJSON.
  map.data.loadGeoJson(href = 'api.jsonserve.com/AAUwWg');
  // Color each letter gray. Change the color when the isColorful property
  // is set to true.
  map.data.setStyle({
    fillColor: '#2687bf',
    fillOpacity: .3,
    strokeWeight: 0
  });
  // When the user clicks, set 'isColorful', changing the color of the letters.
  //map.data.addListener("click", (event) => {
  //  event.feature.setProperty("isColorful", true);
  //});
  // When the user hovers, tempt them to click by outlining the letters.
  // Call revertStyle() to remove all overrides. This will use the style rules
  // defined in the function passed to setStyle()
 // map.data.addListener("mouseover", (event) => {
 //   map.data.revertStyle();
 //   map.data.overrideStyle(event.feature, { strokeWeight: 8 });
 // });
  //map.data.addListener("mouseout", (event) => {
  //  map.data.revertStyle();
 // });
  
}

window.initMap = initMap;

