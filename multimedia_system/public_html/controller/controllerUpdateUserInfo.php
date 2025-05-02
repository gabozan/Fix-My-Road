<?php

if (!isset($_SESSION['id_user'])) {
    header("Location: index.php?action=resource-login");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/checkUpdateUserInfo.php";

    $userId = $_SESSION['id_user'];
    $name = $_POST['name'];
    $email = $_POST['email'];
    $errors = [];

    $connection = connectDB();

    if (isUsernameTakenByOtherUser($connection, $name, $userId)) {
        $errors[] = "El nombre de usuario ya está en uso.";
    }

    if (isEmailTakenByOtherUser($connection, $email, $userId)) {
        $errors[] = "El correo electrónico ya está en uso.";
    }

    if (empty($errors)) {
        $result = updateUser($connection, $userId, $email, $name);

        if ($result) {
            $_SESSION["user_email"] = $email;
            header("Location: index.php?action=resource-myAccount");
            exit();
        } else {
            $errors[] = "Hubo un problema al actualizar la información.";
        }
    }

    $_SESSION['update_user_errors'] = $errors;
    $_SESSION['update_user_old'] = [
        'name' => $name,
        'email' => $email,
    ];
    header("Location: index.php?action=resource-myAccount");
    exit();
}
