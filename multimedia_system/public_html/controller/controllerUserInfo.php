<?php

if (!isset($_SESSION['id_user'])) {
    header("Location: index.php?action=resource-login");
    exit();
}

require_once __DIR__ . "/../model/connectDB.php";
require_once __DIR__ . "/../model/checkUserInfo.php";

$userId = $_SESSION['id_user'] ?? null;

$connection = connectDB();
$userData = getUserInfo($connection, $userId);

require __DIR__ . "/../view/printMyAccount.php";
pg_close($connection);

?>