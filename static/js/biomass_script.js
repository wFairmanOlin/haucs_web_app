let map;

// Function that styles the boxes given their last voltage
function boxStyle(pond_id,voltage) {
  var mediumBatt = 3.7;
  var lowBatt = 3.4;
  let color = 'gray';

    if (voltage<=lowBatt){
      color = 'red';
    }

    else if(voltage>lowBatt & voltage<=mediumBatt){
      color = 'orange';
    }

    else if(voltage>mediumBatt){
      color = "green";
    }

    return color;
  }
  
// Function that initializes the map
function initMap() {
  var center = { lat: 27.5292996, lng: -80.3512828 };
  var map = new google.maps.Map(document.getElementById('map'), 
  {
    zoom: 20,
    center: center,
    mapTypeId: 'satellite',
    mapTypeControl: false,
    fullscreenControl: false,
    streetViewControl: false
  });

  // Load GeoJSON.
  map.data.addGeoJson(geoFile_bms);

  map.data.setStyle((feature) => {
    let pond_id = feature.getProperty('number');
    let voltage = battVolt_bms[pond_id]

    color = boxStyle(pond_id, voltage)
   
    return /** @type {!google.maps.Data.StyleOptions} */ {
      fillColor: color,
      strokeColor: color,
      strokeWeight: 2,
    };
  });

  //Adding listeners for user interaction
  map.data.addListener("click", (event) => {
    location.href = "/sensor"+event.feature.getProperty("number");
  });

  map.data.addListener("mouseover", (event) => {
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, { strokeWeight: 5 });
  });

  map.data.addListener("mouseout", (event) => {
    map.data.revertStyle();
  });
}

window.initMap = initMap;