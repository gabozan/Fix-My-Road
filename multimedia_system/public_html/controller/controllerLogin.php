<?php

// Se inicializa un array para almacenar posibles errores de validación o autenticación.
$errors = [];

// Se comprueba si la solicitud se ha hecho mediante el método POST, lo que indica que el formulario ha sido enviado.
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Se importan los módulos necesarios: conectarse a la base de datos y obtener el usuario a partir del correo electrónico.
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/m_login.php";
    
    // Se recogen los datos enviados desde el formulario.
    $email = $_POST['email'];
    $password = $_POST['password'];
    
    // Se verifica que no esté vacío y formato válido de correo electrónico.
    if (empty($email)) {
        $errors[] = "El campo 'Correo electrónico' no puede estar vacío.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "El correo electrónico no tiene un formato válido.";
    }

    // - Se verifica que no esté vacío.
    if (empty($password)) {
        $errors[] = "El campo 'Contraseña' es obligatorio.";
    }

    // Si no hay errores de validación, se procede con la autenticación del usuario.
    if (empty($errors)) {
        // Se conecta a la base de datos y se busca el usuario en la base de datos por su correo.
        $connection = connectDB();
        $user = loginUser($email, $connection);
        
        // Si el usuario existe y la contraseña es correcta, se inicia sesión y se redirige al index.
        if ($user && password_verify($password, $user["password"])) {
            $_SESSION["id_user"] = $user["id_user"];
            $_SESSION["user_email"] = $user["email"];
            header("Location: index.php");
            exit();

        // Si las credenciales no son válidas, se añade un mensaje de error.
        } else {
            $errors[] = "Correo electrónico o contraseña incorrectos.";
        }
    }
}

// Finalmente, se carga la vista que muestra el formulario de login y los posibles errores.
require __DIR__ . "/../view/printLogin.php";
?>