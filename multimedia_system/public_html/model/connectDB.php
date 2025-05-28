<?php

// Función para establecer la conexión con la base de datos PostgreSQL.
// Define los parámetros necesarios (host, puerto, nombre de la base, usuario, contraseña y modo SSL).
// Intenta conectar usando pg_connect con esos parámetros.
// Si falla, muestra un error y detiene la ejecución.
// Devuelve el recurso de conexión para usarlo en otras consultas.
function connectDB(){
    $server = "34.175.21.104";
    $port = "5432";
    $DBname = "postgres";
    $user = "postgres";
    $password = "1234";
    $sslmode = "require";

    $connection = pg_connect("host=$server port=$port dbname=$DBname user=$user password=$password sslmode=$sslmode") or die("Error de conexión a la base de datos");

    return $connection;
}
?>
