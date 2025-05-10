<?php

$errors = [];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/m_login.php";
    
    $email = $_POST['email'];
    $password = $_POST['password'];
    
    if (empty($email)) {
        $errors[] = "El campo 'Correo electrónico' no puede estar vacío.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "El correo electrónico no tiene un formato válido.";
    }

    if (empty($password)) {
        $errors[] = "El campo 'Contraseña' es obligatorio.";
    }

    if (empty($errors)) {
        $connection = connectDB();
        $user = loginUser($email, $connection);
        
        if ($user && password_verify($password, $user["password"])) {
            $_SESSION["id_user"] = $user["id_user"];
            $_SESSION["user_email"] = $user["email"];
            header("Location: index.php");
            exit();
        } else {
            $errors[] = "Correo electrónico o contraseña incorrectos.";
        }
    }
}
require __DIR__ . "/../view/printLogin.php";
?>