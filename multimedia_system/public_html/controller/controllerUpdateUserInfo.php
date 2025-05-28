<?php
// Verifica que el usuario haya iniciado sesión. Si no, redirige al login.
if (!isset($_SESSION['id_user'])) {
    header("Location: index.php?action=resource-login");
    exit();
}

// Si el formulario se envió por método POST:
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Se incluyen los módulos necesarios: conexión a la base de datos y para la lógica de actualización de información de usuario.
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/checkUpdateUserInfo.php";

    // Se obtienen los datos del formulario y el ID del usuario desde la sesión.
    $userId = $_SESSION['id_user'];
    $name = $_POST['name'];
    $email = $_POST['email'];
    $errors = [];

    $connection = connectDB();

    // Se valida que el correo no esté ya registrado por otro usuario distinto al actual.
    if (isEmailTakenByOtherUser($connection, $email, $userId)) {
        $errors[] = "El correo electrónico ya está en uso.";
    }

    // Si no hay errores, se procede a actualizar el nombre y correo en la base de datos.
    if (empty($errors)) {
        $result = updateUser($connection, $userId, $email, $name);

        // Si la actualización fue exitosa, actualiza el email en la sesión y redirige.
        if ($result) {
            $_SESSION["user_email"] = $email;
            header("Location: index.php?action=resource-myAccount");
            exit();

        // Si falla la actualización, añade un error.
        } else {
            $errors[] = "Hubo un problema al actualizar la información.";
        }
    }

    // Si hubo errores, se guardan en la sesión para mostrarlos después, junto con los datos introducidos para no perderlos en el formulario.
    $_SESSION['update_user_errors'] = $errors;
    $_SESSION['update_user_old'] = [
        'name' => $name,
        'email' => $email,
    ];

    // Se redirige a la página de cuenta para mostrar resultados o errores.
    header("Location: index.php?action=resource-myAccount");
    exit();
}
