<?php
// Verifica si se han recibido correctamente los parámetros 'email' y 'name' desde Google.
// Si no están presentes, redirige al login con un error.
if (!isset($_GET['email']) || !isset($_GET['name'])) {
    header("Location: index.php?action=login&error=missing_google_data");
    exit();
}

// Se importan los módulos necesarios: conectarse a la base de datos y obtener el usuario a partir del correo electrónico.
require_once __DIR__ . "/../model/connectDB.php";
require_once __DIR__ . "/../model/m_userGoogle.php";

// Se recuperan los datos enviados por Google mediante GET.
$email = $_GET['email'];
$name = $_GET['name'];

// Se establece la conexión con la base de datos y se busca si ya existe un usuario con ese email.
$connection = connectDB();
$user = getUserByEmail($connection, $email);

// Si el usuario ya existe en la base de datos e guardan sus datos en la sesión y se redirige al inicio.
if ($user) {
    $_SESSION['user_name'] = $user['name'];
    $_SESSION['id_user'] = $user['id_user'];
    $_SESSION['user_email'] = $user['email'];

    header("Location: index.php?action=home");
    exit();

// Si el usuario no existe se redirige al formulario de registro con los datos ya precargados en la URL.
} else {
    $redirect = "index.php?action=resource_register_google&name=" . urlencode($name) . "&email=" . urlencode($email);
    header("Location: $redirect");
    exit();
}
