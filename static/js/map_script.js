let map;

function boxStyle() {
  var mediumBatt = 3.7;
  var lowBatt = 3.4;

  for (i=0; i<battVolt;i++){
    if (battVolt[i]<lowBatt){
      fillColor : "red"
    }

    else if(battVolt[i]>lowBatt & battVolt[i]<mediumBatt){
      fillColor :  "orange"
    }

    else{
      fillColor : "green"
    }
  }
}

function initMap() {
  var center = { lat: 27.529283711906945, lng: -80.35124747779686 };

  var map = new google.maps.Map(document.getElementById('map'), 
  {
    zoom: 20,
    center: center,
    mapTypeId: 'satellite'
  });

  

  // Load GeoJSON.
  map.data.addGeoJson(geoFile);

  // Color each letter gray. Change the color when the isColorful property
  // is set to true.
  map.data.setStyle({
    
    boxStyle})

    // fillColor: "green",
    // strokeWeight: 2
    
    // for (i=0;i< battVolt; i++) {
    //   print(battVolt[i])
    // }

    // // if (feature.getProperty("isColorful")) {
    // //   color = feature.getProperty("color");
    // // }
    // // return /** @type {!google.maps.Data.StyleOptions} */ {
    // //   fillColor: color,
    // //   strokeColor: color,
    // //   strokeWeight: 2,
    // // };

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