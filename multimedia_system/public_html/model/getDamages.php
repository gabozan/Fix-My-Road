<?php
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
