<?php

function updateUser($connection, $userId, $email, $name) {
    $sql = 'UPDATE "user" SET email = $1, name = $2 WHERE id_user = $3';
    $params = [$email, $name, $userId];
    return pg_query_params($connection, $sql, $params);
}

function updatePassword($connection, $userId, $password) {
    $passwordHash = password_hash($password, PASSWORD_DEFAULT);
    $sql = 'UPDATE "user" SET password = $1 WHERE id_user = $2';
    $params = [$passwordHash, $userId];
    return pg_query_params($connection, $sql, $params);
}

?>
