<?php

// Función para obtener toda la información de un usuario a partir de su correo electrónico.
// Recibe la conexión a la base de datos y el email del usuario a buscar.
// Ejecuta una consulta parametrizada para evitar inyección SQL.
// Devuelve un array asociativo con los datos del usuario si se encuentra, o null si no.
function getUserByEmail($connection, $email) {
    $sql = "SELECT * FROM \"user\" WHERE email = $1";
    $query = pg_query_params($connection, $sql, [$email]) or die("Error al ejecutar la consulta de usuario por email.");
    $result = pg_fetch_assoc($query);
    return $result;
}