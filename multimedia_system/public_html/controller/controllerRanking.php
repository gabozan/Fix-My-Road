<?php

require_once __DIR__ . "/../model/connectDB.php";
require_once __DIR__ . "/../model/checkRanking.php";

$connection = connectDB();
$topRanking = getTopRanking($connection);

$userRanking = null;
if (isset($_SESSION['id_user'])) {
    $userRanking = getUserRanking($connection, $_SESSION['id_user']);
}

pg_close($connection);

require __DIR__ . "/../view/printRanking.php";
?>
