<?php

// Función para actualizar el email y nombre de un usuario específico.
// Recibe conexión, id del usuario, nuevo email y nuevo nombre.
// Ejecuta una consulta parametrizada para evitar inyección SQL.
// Parámetros:
// - $connection: recurso de conexión a la base de datos PostgreSQL.
// - $userId: identificador único del usuario a actualizar.
// - $email: nuevo email que se asignará al usuario.
// - $name: nuevo nombre que se asignará al usuario.
function updateUser($connection, $userId, $email, $name) {
    $sql = 'UPDATE "user" SET email = $1, name = $2 WHERE id_user = $3';
    $params = [$email, $name, $userId];
    return pg_query_params($connection, $sql, $params);
}

// Función para actualizar la contraseña de un usuario.
// Recibe conexión, id del usuario y la nueva contraseña en texto plano.
// Hashea la contraseña antes de almacenarla para seguridad.
// Ejecuta una consulta parametrizada para actualizar el campo password.
// Parámetros:
// - $connection: recurso de conexión a la base de datos PostgreSQL.
// - $userId: identificador único del usuario cuya contraseña será actualizada.
// - $password: nueva contraseña en texto plano que se hasheará antes de guardarla.
function updatePassword($connection, $userId, $password) {
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);
    $sql = 'UPDATE "user" SET password = $1 WHERE id_user = $2';
    $params = [$passwordHash, $userId];
    return pg_query_params($connection, $sql, $params);
}

// Función para verificar si un nombre de usuario ya está en uso por otro usuario distinto.
// Utiliza una consulta parametrizada para buscar coincidencias de nombre que no pertenezcan al usuario actual.
// Retorna true si encuentra otro usuario con el mismo nombre, false si no.
// Parámetros:
// - $connection: recurso de conexión a la base de datos PostgreSQL.
// - $username: nombre de usuario a comprobar.
// - $currentUserId: id del usuario actual para excluirlo de la comprobación.
function isUsernameTakenByOtherUser($connection, $username, $currentUserId) {
    $sql = 'SELECT 1 FROM "user" WHERE name = $1 AND id_user != $2';
    $result = pg_query_params($connection, $sql, [$username, $currentUserId]);
    return pg_num_rows($result) > 0;
}

// Función similar a la anterior, pero para verificar si un email está en uso por otro usuario distinto.
// Retorna true si el email está ocupado por otro usuario.
// Parámetros:
// - $connection: recurso de conexión a la base de datos PostgreSQL.
// - $email: email a comprobar.
// - $userId: id del usuario actual para excluirlo de la comprobación.
function isEmailTakenByOtherUser($connection, $email, $userId) {
    $sql = 'SELECT 1 FROM "user" WHERE email = $1 AND id_user != $2';
    $result = pg_query_params($connection, $sql, [$email, $userId]);
    return pg_num_rows($result) > 0;
}

?>
