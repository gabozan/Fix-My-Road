<?php

// Función para obtener información básica de un usuario a partir de su ID.
// Recibe la conexión a la base de datos y el ID del usuario.
// Ejecuta una consulta parametrizada para traer el nombre y correo electrónico.
// Retorna un array asociativo con los datos del usuario o false si no existe.
// Parámetros:
// - $connection: recurso de conexión a la base de datos PostgreSQL.
// - $userId: identificador único del usuario a consultar.
function getUserInfo($connection, $userId) {
    $sql_account = 'SELECT name, email FROM "user" WHERE id_user = $1';
    $query_account = pg_query_params($connection, $sql_account, [$userId]) or die("Error al ejecutar la consulta de datos de cuenta.");
    $result_account = pg_fetch_assoc($query_account);
    return $result_account;
}

?>
