<?php
function getUserByEmail($connection, $email) {
    $sql = "SELECT * FROM \"user\" WHERE email = $1";
    $query = pg_query_params($connection, $sql, [$email]) or die("Error al ejecutar la consulta de usuario por email.");
    $result = pg_fetch_assoc($query);
    return $result;
}