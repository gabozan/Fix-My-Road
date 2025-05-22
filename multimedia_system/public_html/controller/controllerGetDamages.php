<?php
require_once __DIR__ . '/../model/connectDB.php';
require_once __DIR__ . '/../model/getDamages.php';

$connection = connectDB();
$damages = getDamages($connection);

header('Content-Type: application/json');
echo json_encode($damages);

pg_close($connection);
?>
