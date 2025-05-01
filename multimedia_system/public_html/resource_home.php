<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fix my road - Inicio</title>
  <link rel="icon" href="/assets/imgs/logo_Fix-my-road_no_background.png">
  <link rel="stylesheet" href="assets/css/global.css">
  <link rel="stylesheet" href="assets/css/home.css">
  <link rel="stylesheet" href="assets/css/legend.css">
  <link rel="stylesheet" href="assets/css/info-box.css">
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="/assets/js/userAction.js"></script>
</head>
<body>
  <?php require __DIR__ . "/controller/controllerHeader.php" ?>
  
  <main>
    <h1>🌍 Mapa Interactivo</h1>

    <div id="google-map"></div>
    <script src="../mapsJavascriptAPI.js" defer></script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC4YMWh8KpycM8gmFRuhIqhxP7uN8Wwj1Y&callback=initMap" defer></script>
    <div id="map-info" style="background: #f0f8ff; padding: 1.5em; border-radius: 8px; margin: 2em auto; max-width: 800px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: sans-serif;"> <p style="margin-bottom: 1em;">
      🗺️ En este <strong>mapa interactivo</strong> puedes visualizar distintos <strong>daños en la vía pública</strong> como <em>baches</em>, <em>grietas</em> y <em>fisuras</em>. </p> <ul style="padding-left: 1.2em;"> <li>📍 Haz <strong>clic en cualquier icono</strong> del mapa para ver los detalles.</li> <li>🖼️ Se mostrará una <strong>imagen del daño</strong> real.</li> <li>📬 También verás la <strong>dirección exacta</strong> donde se ha reportado.</li> </ul> <p style="margin-top: 1em;"> 📢 Si detectas una nueva incidencia, ¡no dudes en reportarla desde el menú superior! </p> 
    </div>
  </main>

  <?php require __DIR__ . "/controller/controllerFooter.php" ?>

</body>
</html>
