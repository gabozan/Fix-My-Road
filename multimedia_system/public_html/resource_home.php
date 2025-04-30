<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mapa con Marcadores</title>
  <style>
    html, body { height: 100%; margin: 0; padding: 0; }
    #google-map { width: 100%; height: 500px; }
  </style>
</head>
<body>
  <h1 style="text-align:center;">Mapa Interactivo</h1>
  <div id="google-map"></div>
  <script src="../mapsJavascriptAPI.js"></script>
  <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC4YMWh8KpycM8gmFRuhIqhxP7uN8Wwj1Y&callback=initMap">
  </script>
</body>
</html>
