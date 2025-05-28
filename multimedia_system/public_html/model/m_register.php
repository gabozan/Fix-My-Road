<?php

// Función para registrar un nuevo usuario en la base de datos.
// Recibe nombre, correo, contraseña y la conexión a la base de datos.
// La contraseña se encripta con password_hash para seguridad antes de guardarla.
// Inserta el nuevo usuario en la tabla "user" usando consulta parametrizada para evitar inyección SQL.
// Devuelve el resultado de la operación (true si tuvo éxito, false si no).
function registerUser($name, $email, $password, $connection) {
    $password = password_hash($password, PASSWORD_DEFAULT);
    $sql = 'INSERT INTO "user" (name, email, password) VALUES ($1, $2, $3)';
    $params = array($name, $email, $password);
    $result = pg_query_params($connection, $sql, $params);
    return $result;
}

// Función para verificar si un correo electrónico ya está registrado en la base de datos.
// Recibe la conexión y el email a comprobar.
// Ejecuta una consulta que busca cualquier registro con ese email.
// Retorna true si el email ya existe (es decir, hay alguna fila) y false si no.
function isEmailTaken($connection, $email) {
    $sql = 'SELECT 1 FROM "user" WHERE email = $1';
    $result = pg_query_params($connection, $sql, [$email]);
    return pg_num_rows($result) > 0;
}

?>
