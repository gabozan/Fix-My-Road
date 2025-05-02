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

function isUsernameTakenByOtherUser($connection, $username, $currentUserId) {
    $sql = 'SELECT 1 FROM "user" WHERE name = $1 AND id_user != $2';
    $result = pg_query_params($connection, $sql, [$username, $currentUserId]);
    return pg_num_rows($result) > 0;
}

function isEmailTakenByOtherUser($connection, $email, $userId) {
    $sql = 'SELECT 1 FROM "user" WHERE email = $1 AND id_user != $2';
    $result = pg_query_params($connection, $sql, [$email, $userId]);
    return pg_num_rows($result) > 0;
}

?>
