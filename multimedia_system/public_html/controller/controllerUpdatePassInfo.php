<?php
// Si no hay una sesión activa, se redirige al login.
if (!isset($_SESSION['id_user'])) {
    header("Location: index.php?action=resource-login");
    exit();
}

// Si se ha enviado el formulario de cambio de contraseña mediante POST:
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Se incluyen los módulos necesarios: establecer la conexión con la base de datos y importa la lógica para actualizar datos del usuario.
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/checkUpdateUserInfo.php";

    // Se obtienen los datos del formulario.
    $userId = $_SESSION['id_user'];
    $password = $_POST['password'];
    $confirmPassword = $_POST['confirm_password'];

    // Se verifica que ambas contraseñas coincidan.
    if ($password === $confirmPassword) {
        $connection = connectDB();
        $result = updatePassword($connection, $userId, $password);

        // Se conecta a la base de datos y se actualiza la contraseña.
        if ($result) {
            header("Location: index.php?action=resource-myAccount&success=password");
            exit();
        }
    }
}

// Si la solicitud no es POST o las contraseñas no coinciden, se redirige de nuevo a la cuenta.
header("Location: index.php?action=resource-myAccount");
exit();

?>
