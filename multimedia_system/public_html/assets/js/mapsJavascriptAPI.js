function initMap() {
  //Recibimos de la bd, las coordenadas y dirección de la grieta.
  //markers es un array de objetos que contiene la información de los marcadores a mostrar en el mapa.
  const markers = [
    {
      locationName: 'Flat White',
      lat: 51.5139,
      lng: -0.1337,
      address: '17 Berwick St,<br>London,<br>W1F 0PT'
    },
    {
      locationName: 'Sacred Coffee',
      lat: 51.5157,
      lng: -0.1394,
      address: '13 Ganton St,<br>London,<br>W1F 9BL'
    },
    {
      locationName: 'Department of Coffee and Social Affairs',
      lat: 51.5145,
      lng: -0.1392,
      address: '3 Lowndes Ct,<br>London,<br>W1F 7HD'
    },
    {
      locationName: 'Kaffeine',
      lat: 51.5161,
      lng: -0.1399,
      address: '15 Eastcastle St,<br>London,<br>W1T 3AY'
    }
  ];
  
  const centerMap = { lat: 51.5034984, lng: -0.1198804 }
  mapOptions = {
    center: centerMap,
    zoom: 10,
    disableDefaultUI: true,
    styles: [
      {
          "featureType": "water",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#e9e9e9"
              },
              {
                  "lightness": 17
              }
          ]
      },
      {
          "featureType": "landscape",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#f5f5f5"
              },
              {
                  "lightness": 20
              }
          ]
      },
      {
          "featureType": "road.highway",
          "elementType": "geometry.fill",
          "stylers": [
              {
                  "color": "#ffffff"
              },
              {
                  "lightness": 17
              }
          ]
      },
      {
          "featureType": "road.highway",
          "elementType": "geometry.stroke",
          "stylers": [
              {
                  "color": "#ffffff"
              },
              {
                  "lightness": 29
              },
              {
                  "weight": 0.2
              }
          ]
      },
      {
          "featureType": "road.arterial",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#ffffff"
              },
              {
                  "lightness": 18
              }
          ]
      },
      {
          "featureType": "road.local",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#ffffff"
              },
              {
                  "lightness": 16
              }
          ]
      },
      {
          "featureType": "poi",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#f5f5f5"
              },
              {
                  "lightness": 21
              }
          ]
      },
      {
          "featureType": "poi.park",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#dedede"
              },
              {
                  "lightness": 21
              }
          ]
      },
      {
          "elementType": "labels.text.stroke",
          "stylers": [
              {
                  "visibility": "on"
              },
              {
                  "color": "#ffffff"
              },
              {
                  "lightness": 16
              }
          ]
      },
      {
          "elementType": "labels.text.fill",
          "stylers": [
              {
                  "saturation": 36
              },
              {
                  "color": "#333333"
              },
              {
                  "lightness": 40
              }
          ]
      },
      {
          "elementType": "labels.icon",
          "stylers": [
              {
                  "visibility": "off"
              }
          ]
      },
      {
          "featureType": "transit",
          "elementType": "geometry",
          "stylers": [
              {
                  "color": "#f2f2f2"
              },
              {
                  "lightness": 19
              }
          ]
      },
      {
          "featureType": "administrative",
          "elementType": "geometry.fill",
          "stylers": [
              {
                  "color": "#fefefe"
              },
              {
                  "lightness": 20
              }
          ]
      },
      {
          "featureType": "administrative",
          "elementType": "geometry.stroke",
          "stylers": [
              {
                  "color": "#fefefe"
              },
              {
                  "lightness": 17
              },
              {
                  "weight": 1.2
              }
          ]
      }
  ]
  }

  const map = new google.maps.Map(
    document.getElementById('google-map'),mapOptions
  );

  const legend = document.createElement('div');
  legend.id = 'legend';
  legend.innerHTML = `
    <ul>
      <li><img src="../../assets/señal_bache.png" alt="">Bache</li>
      <li><img src="../../assets/señal_cocodrilo.png" alt="">Grieta</li>
      <li><img src="../../assets/señal_grieta_longitudinal.png" alt="">Grieta longitudinal</li>
      <li><img src="../../assets/señal_grieta_transversal.png" alt="">Grieta transversal</li>
    </ul>
  `;
  google.maps.event.addListenerOnce(map, 'idle', function() {
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
  });


  const fehMarker = "../../assets/señal_bache.png";
  const infoWindow = new google.maps.InfoWindow({
    minWidth: 200,
    maxWidth: 200
  });
  const bounds = new google.maps.LatLngBounds();
  for(let i = 0; i < markers.length; i++) {
    const marker = new google.maps.Marker({
      position: { lat: markers[i]['lat'], lng: markers[i]['lng'] },
      map: map,
      icon: {
        url: fehMarker,
        scaledSize: new google.maps.Size(50, 50) 
      }
    });
    const content = `
      <div class="feh-content">
        <h2></h2>
      </div>
    `;
    function createInfoWindow(){
      google.maps.event.addListener(marker, 'click', function(){
        infoWindow.setContent(content);
        infoWindow.open(map, marker);
      });
    }
    createInfoWindow();

    infoWindow.addListener('closeclick', function() {
      map.fitBounds(bounds);
    });
    bounds.extend(new google.maps.LatLng(markers[i]['lat'], markers[i]['lng']));
    map.fitBounds(bounds);
  }
}
