<?php

if (!isset($_GET['email']) || !isset($_GET['name'])) {
    header("Location: index.php?action=login&error=missing_google_data");
    exit();
}

require_once __DIR__ . "/../model/connectDB.php";
require_once __DIR__ . "/../model/m_userGoogle.php";

$email = $_GET['email'];
$name = $_GET['name'];

$connection = connectDB();
$user = getUserByEmail($connection, $email);

if ($user) {
    $_SESSION['user_name'] = $user['name'];
    $_SESSION['id_user'] = $user['id_user'];
    $_SESSION['user_email'] = $user['email'];

    header("Location: index.php?action=home");
    exit();
} else {
    $redirect = "index.php?action=resource_register_google&name=" . urlencode($name) . "&email=" . urlencode($email);
    header("Location: $redirect");
    exit();
}
