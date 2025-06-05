<?php

// Función para obtener los datos del usuario a partir de su correo electrónico.
// Recibe el email y la conexión a la base de datos.
// Ejecuta una consulta segura (pg_query_params) para buscar el usuario con ese email en la tabla "user".
// Devuelve un array asociativo con los datos del usuario (id_user, email y password hashed).
// Si no encuentra usuario, devuelve null.
// Parámetros:
// - $email: correo electrónico del usuario (string).
// - $connection: recurso de conexión a la base de datos PostgreSQL.
function loginUser($email, $connection) {
    $sql_user = 'SELECT id_user, email, password FROM "user" WHERE email = $1';
    $query_user = pg_query_params($connection, $sql_user, [$email]) or die("Error al ejecutar la consulta de usuario.");
    $result_user = pg_fetch_assoc($query_user);
    return $result_user;
}

?>