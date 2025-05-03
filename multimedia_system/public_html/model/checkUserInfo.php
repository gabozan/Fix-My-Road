<?php

function getUserInfo($connection, $userId) {
    $sql_account = 'SELECT name, email FROM "user" WHERE id_user = $1';
    $query_account = pg_query_params($connection, $sql_account, [$userId]) or die("Error al ejecutar la consulta de datos de cuenta.");
    $result_account = pg_fetch_assoc($query_account);
    return $result_account;
}

?>
