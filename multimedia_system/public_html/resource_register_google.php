<?php
ob_start(); 
?>
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="./assets/imgs/logo_Fix-my-road_no_background-white.png">
        <link rel="stylesheet" href="assets/css/global.css">
        <link rel="stylesheet" href="assets/css/register.css">
        <title>Fix my road - Registro Google</title>
    </head>
    <body>
        <?php require __DIR__ . "/controller/controllerHeader.php" ?>

        <main>
            <?php require __DIR__ . "/controller/controllerRegisterGoogle.php" ?>
        </main>

        <?php require __DIR__ . "/controller/controllerFooter.php" ?>
    </body>
</html>
<?php
ob_end_flush(); // Opcional, pero recomendable para cerrar el buffer manualmente
?>
