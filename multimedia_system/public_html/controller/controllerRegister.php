<?php
// Array donde se guardarán los posibles errores de validación.
$errors = [];

// Se comprueba si el formulario ha sido enviado mediante POST.
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Se cargan los módulos necesarios: conectarse a la base de datos y se obtienen las funciones para validar y registrar usuarios.
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/m_register.php";

    // Se extraen los datos enviados desde el formulario.
    $name = $_POST['name']; 
    $email = $_POST['email']; 
    $password = $_POST['password']; 

    // Se verifica que ningún campo esté vacío y se comprueba que el email tenga un formato válido.
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

    // Se verifica que el correo no esté ya registrado en la base de datos.
    $connection = connectDB();
    if (isEmailTaken($connection, $email)) {
        $errors[] = "El correo electrónico ya está en uso.";
    }

    // Si no hay errores, se intenta registrar al nuevo usuario.
    if (empty($errors)) {
        $result = registerUser($name, $email, $password, $connection);

        // Si el registro fue exitoso, se redirige al inicio.
        if ($result) {
            header("Location: index.php");
            exit();

        // Si ocurre un error durante el registro, se añade un mensaje de error.
        } else {
            $errors[] = "Hubo un problema al registrar al usuario. Inténtalo de nuevo.";
        }
    }
}

// Finalmente, se carga la vista del formulario de registro con los errores.
require __DIR__ . "/../view/printRegister.php";
?>
