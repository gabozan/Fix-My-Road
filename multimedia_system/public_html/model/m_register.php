<?php

function registerUser($name, $email, $password, $connection) {
    $password = password_hash($password, PASSWORD_DEFAULT);
    $sql = 'INSERT INTO "user" (name, email, password) VALUES ($1, $2, $3)';
    $params = array($name, $email, $password);
    $result = pg_query_params($connection, $sql, $params);
    return $result;
}

function isEmailTaken($connection, $email) {
    $sql = 'SELECT 1 FROM "user" WHERE email = $1';
    $result = pg_query_params($connection, $sql, [$email]);
    return pg_num_rows($result) > 0;
}

?>
