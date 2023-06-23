let map;

// Function that styles the boxes given their last voltage
function boxStyle(pond_id,voltage) {
  var mediumBatt = 3.7;
  var lowBatt = 3.4;
  let color = 'gray';

    if (voltage<=lowBatt){
      color = 'red';
    }

    else if(voltage>=lowBatt & voltage<mediumBatt){
      color = 'orange';
    }

    else if(voltage>=mediumBatt){
      color = "green";
    }

    return color;
  }
  
// Function that initializes the map
function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), 
  {
    zoom: 16,
    center: { lat: 37.7037823, lng: -89.4648105 },
    mapTypeId: 'satellite',
    mapTypeControl: false,
    fullscreenControl: false,
    streetViewControl: false
    // mapId: 'DEMO_MAP_ID'
  });

  // Load GeoJSON.
  map.data.addGeoJson(geoFile_HAUCS);

  map.data.setStyle((feature) => {
    let pond_id = feature.getProperty('number');
    let voltage = battVolt_HAUCS[pond_id]

    color = boxStyle(pond_id, voltage)
   
    return /** @type {!google.maps.Data.StyleOptions} */ {
      fillColor: color,
      strokeColor: color,
      strokeWeight: 2,
    };
  });

  const markers = [
    [ 37.7037823, -89.4648105],
    [ 37.703000518448896, -89.4688201254245]
  ];

  var status="off"; //will be a data point sent eventually
  var marker=[];
  var marker_icon = '';

  function createMarkers(status, markers, marker_icon){
    
    for(let i=0; i<markers.length; i++){
      const currMarker = markers[i];
      if (status=='on'){
        marker_icon = "static/aerator_on.svg";
      }
      else{
        marker_icon = "static/aerator_off.svg";
      }
      
      marker = new google.maps.Marker({
        position: {lat: currMarker[0], lng: currMarker[1]},
        map,
        icon: {
          url: marker_icon,
          scaledSize: new google.maps.Size(25,25)
        }
      }) 

      // const infoWindow = new google.maps.InfoWindow({
      //   content: 'Status: '
      // });
        
      // marker.addListener("click",() => {
      //   infoWindow.setContent('Status: ')
      //   infoWindow.open(map,marker);
      // });
    }
  }

  // Setting up markers
  map_markers = createMarkers(status, markers, marker_icon)

  }

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


window.initMap = initMap;