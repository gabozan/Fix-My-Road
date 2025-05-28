<?php
// Se importan los módulos del modelo: establecer conexión con la base de datos y obtener daños.
require_once __DIR__ . '/../model/connectDB.php';
require_once __DIR__ . '/../model/getDamages.php';

// Se conecta a la base de datos y se obtiene la lista de daños.
$connection = connectDB();
$damages = getDamages($connection);

// Se prepara la respuesta JSON y se envían los datos convertidos a este formato.
header('Content-Type: application/json');
echo json_encode($damages);

// Se cierra la conexión con la base de datos una vez finalizado el proceso.
pg_close($connection);
?>
