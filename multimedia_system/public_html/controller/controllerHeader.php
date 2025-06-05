<?php

// Este controlador verifica si el usuario ha iniciado sesión (almacenando el resultado en $isLoggedIn)
// y luego carga la vista del encabezado (header) del sitio web.
$isLoggedIn = isset($_SESSION['id_user']);
require __DIR__ . "/../view/printHeader.php";

?>