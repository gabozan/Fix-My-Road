<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Fix my road - Inicio</title>
  <link rel="icon" href="./assets/imgs/logo_Fix-my-road_no_background-white.png">
  <link rel="stylesheet" href="assets/css/global.css">
  <link rel="stylesheet" href="assets/css/home.css">
  
</head>
<body>
  <?php require __DIR__ . "/controller/controllerHeader.php" ?>
  
  <main>
    <?php require __DIR__ . "/controller/controllerHomeMap.php" ?>
  </main>

  <?php require __DIR__ . "/controller/controllerFooter.php" ?>

  <script src="assets/js/mapsJavascriptAPI.js"></script>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC4YMWh8KpycM8gmFRuhIqhxP7uN8Wwj1Y&callback=initMap" defer></script>
</body>
</html>
