<?php
function connectDB(){
    $server = "";
    $port = "";
    $DBname = "";
    $user = "";
    $password = "";
    $connection = pg_connect("host=$server port=$port dbname=$DBname user=$user password=$password") or die("Error de conección a la base de datos");
    return($connection);
}
?>