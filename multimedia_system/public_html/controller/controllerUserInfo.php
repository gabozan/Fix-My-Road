<?php
// Primero verifica que el usuario haya iniciado sesión. Si no, lo redirige a la página de login.
if (!isset($_SESSION['id_user'])) {
    header("Location: index.php?action=resource-login");
    exit();
}

// Incluye los modelos necesarios para conectar a la base de datos
// y para obtener la información del usuario.
require_once __DIR__ . "/../model/connectDB.php";
require_once __DIR__ . "/../model/checkUserInfo.php";

// Obtiene el ID del usuario de la sesión.
$userId = $_SESSION['id_user'] ?? null;

// Establece conexión con la base de datos y obtiene los datos del usuario.
$connection = connectDB();
$userData = getUserInfo($connection, $userId);

// Incluye la vista que mostrará los datos del usuario.
require __DIR__ . "/../view/printMyAccount.php";

// Cierra la conexión con la base de datos.
pg_close($connection);

?>