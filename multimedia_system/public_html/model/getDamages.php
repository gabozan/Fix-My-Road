<?php

// Función que obtiene los daños reportados almacenados en la base de datos.
// Recibe la conexión a la base de datos como parámetro.
// Ejecuta una consulta para traer el tipo de daño, URL de la imagen y coordenadas (latitud y longitud) de la tabla "reports".
// Recorre todos los resultados y los transforma en un array asociativo con claves más amigables para el frontend.
// Convierte latitud y longitud a tipo float para precisión.
// Devuelve un array con todos los daños encontrados.
function getDamages($connection) {
    $query = "SELECT damage_type, image_url, latitude, longitude FROM reports";
    $result = pg_query($connection, $query);
    $damages = array();

    while ($row = pg_fetch_assoc($result)) {
        $damages[] = array(
            "damageType" => $row["damage_type"],
            "imageUrl" => $row["image_url"],
            "lat" => floatval($row["latitude"]),
            "lng" => floatval($row["longitude"])
        );
    }
    return $damages;
}
?>
