<?php

function updateUser($connection, $userId, $email, $password, $name, $profilePicturePath) {
    $password = password_hash($password, PASSWORD_DEFAULT);
    $sql = 'UPDATE "user" SET email = $1, password = COALESCE($2, password), name = $3, profile_picture = COALESCE($4, profile_picture) WHERE id_user = $5';
    $params = [$email, $password, $name, $profilePicturePath, $userId];
    $result = pg_query_params($connection, $sql, $params);
    return $result;
}

?>
