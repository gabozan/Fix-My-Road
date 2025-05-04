<?php

function loginUser($email, $connection) {
    $sql_user = 'SELECT id_user, email, password FROM "user" WHERE email = $1';
    $query_user = pg_query_params($connection, $sql_user, [$email]) or die("Error al ejecutar la consulta de usuario.");
    $result_user = pg_fetch_assoc($query_user);
    return $result_user;
}

?>