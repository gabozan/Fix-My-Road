function initMap() {
    const centerMap = { lat: 51.5034984, lng: -0.1198804 };
    const mapOptions = {
        center: centerMap,
        zoom: 10,
        disableDefaultUI: true,
        gestureHandling: 'greedy',
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
    };
    const map = new google.maps.Map(document.getElementById('google-map'), mapOptions);

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

    fetch('index.php?action=get-damages')
    .then(response => response.json())
    .then(markers => {
        if (!Array.isArray(markers) || markers.length === 0) {
            alert("No se encontraron daños en la base de datos.");
            return;
        }
        const iconos = {
            bache: "../../assets/señal_bache.png",
            grieta: "../../assets/señal_cocodrilo.png",
            longitudinal: "../../assets/señal_grieta_longitudinal.png",
            transversal: "../../assets/señal_grieta_transversal.png"
        };
        const infoWindow = new google.maps.InfoWindow({
            minWidth: 200,
            maxWidth: 200
        });
        const bounds = new google.maps.LatLngBounds();
        for (let i = 0; i < markers.length; i++) {
            const tipo = markers[i].damageType.toLowerCase();
            const iconoUrl = iconos[tipo] || "../../assets/logo_banner.png";
            const marker = new google.maps.Marker({
                position: { lat: markers[i].lat, lng: markers[i].lng },
                map: map,
                icon: {
                    url: iconoUrl,
                    scaledSize: new google.maps.Size(50, 50)
                }
            });
            const content = `
                <img src="${markers[i].imageUrl || ''}" alt="Daño" style="display:block; width:100%; max-width:260px; height:auto; margin:0 auto;">
            `;
            marker.addListener('click', function() {
                infoWindow.setContent(content);
                infoWindow.open(map, marker);
            });
            bounds.extend(marker.getPosition());
        }
        map.fitBounds(bounds);
        infoWindow.addListener('closeclick', function() {
            map.fitBounds(bounds);
        });
    })
}