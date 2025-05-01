<?php

function registerUser($name, $email, $password, $connection) {
    $password = password_hash($password, PASSWORD_DEFAULT);
    $sql = 'INSERT INTO "user" (name, email, password) VALUES ($1, $2, $3)';
    $params = array($name, $email, $password);
    $result = pg_query_params($connection, $sql, $params);
    return $result;
}

?>
