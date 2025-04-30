<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Mapa Azul</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Segoe UI', sans-serif;
      background-color: #e2e8f0;
      color: #1e293b;
    }

    nav {
      background: linear-gradient(90deg, #3b82f6, #2563eb);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      color: white;
    }

    nav .left a,
    nav .right a {
      text-decoration: none;
      color: white;
      font-weight: 500;
      margin: 0 12px;
      padding: 6px 10px;
      border-radius: 6px;
      transition: background 0.2s ease;
    }

    nav .right {
      display: flex;
      gap: 10px;
    }

    nav a:hover {
      background-color: rgba(255, 255, 255, 0.15);
    }

    h1 {
      text-align: center;
      margin: 30px 0 20px;
      font-size: 26px;
      color: #1e40af;
    }

    #google-map {
        width: 85vw;             /* Ocupa casi todo el ancho visible */
        height: 70vh;            /* Ocupa el 80% de la altura de la pantalla */
        margin: 30px auto;
        padding: 8px;
        background-color: white;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
  </style>
</head>
<body>

  <nav>
    <div class="left">
      <a href="#">🏠 Home</a>
    </div>
    <div class="right">
      <a href="#">Iniciar sesión</a>
      <a href="#">Registrarse</a>
    </div>
  </nav>

  <h1>🌍 Mapa Interactivo</h1>
  <div id="google-map"></div>

  <script src="../mapsJavascriptAPI.js"></script>
  <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC4YMWh8KpycM8gmFRuhIqhxP7uN8Wwj1Y&callback=initMap" async defer></script>
</body>
</html>
