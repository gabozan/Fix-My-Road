<?php

// Este script cierra la sesión del usuario y lo redirige a la página de inicio.
session_unset();
session_destroy();
header("Location: index.php");
exit();

?>