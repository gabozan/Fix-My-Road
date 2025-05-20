<?php
$errors = [];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/m_register.php";

    $name = $_POST['name']; 
    $email = $_POST['email']; 
    $password = $_POST['password']; 

    if (empty($name)) {
        $errors[] = "El campo 'Nombre de usuario' es obligatorio.";
    }

    if (empty($email)) {
        $errors[] = "El campo 'Correo electrónico' no puede estar vacío.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "El correo electrónico no tiene un formato válido.";
    }

    if (empty($password)) {
        $errors[] = "El campo 'Contraseña' es obligatorio.";
    }

    $connection = connectDB();
    if (isEmailTaken($connection, $email)) {
        $errors[] = "El correo electrónico ya está en uso.";
    }

    if (empty($errors)) {
        $result = registerUser($name, $email, $password, $connection);

        if ($result) {
            header("Location: index.php");
            exit();
        } else {
            $errors[] = "Hubo un problema al registrar al usuario. Inténtalo de nuevo.";
        }
    }
}

require __DIR__ . "/../view/printRegister.php";
?>
