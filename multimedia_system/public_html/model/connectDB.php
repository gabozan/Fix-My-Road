<?php
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
