<?php
// Se incluyen los archivos del modelo: se establecer conexión con la base de datos y se obtienen las funciones que consultan el ranking general y el del usuario.
require_once __DIR__ . "/../model/connectDB.php";
require_once __DIR__ . "/../model/checkRanking.php";

// Se establece la conexión a la base de datos y se obtienen los datos del ranking.
$connection = connectDB();
$topRanking = getTopRanking($connection);

// Si hay un usuario logueado, se obtiene su posición individual en el ranking.
$userRanking = null;
if (isset($_SESSION['id_user'])) {
    $userRanking = getUserRanking($connection, $_SESSION['id_user']);
}

// Se cierra la conexión a la base de datos.
pg_close($connection);

// Se carga la vista que muestra el ranking (tanto top como posición del usuario si aplica).
require __DIR__ . "/../view/printRanking.php";
?>
