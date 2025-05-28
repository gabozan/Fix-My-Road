<?php
// Array para almacenar mensajes de error.
$errors = [];

// Solo se ejecuta si el formulario se ha enviado por método POST.
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    // Se cargan los módulos necesarios: conectar con la base de datos y obtener las funciones de validación y registro.
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/m_register.php";

    // Se obtienen los valores enviados desde el formulario de registro.
    $name = $_POST['name']; 
    $email = $_POST['email']; 
    $password = $_POST['password']; 

    // Validación de los campos: que no estén vacíos y que el email tenga formato válido.
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

    // Se conecta a la base de datos y se comprueba si el email ya está registrado.
    $connection = connectDB();
    if (isEmailTaken($connection, $email)) {
        $errors[] = "El correo electrónico ya está en uso.";
    }

    // Si no hay errores de validación, se intenta registrar el nuevo usuario.
    if (empty($errors)) {
        $result = registerUser($name, $email, $password, $connection);

        // Si el registro fue exitoso, se redirige al inicio.
        if ($result) {
            header("Location: index.php");
            exit();

        // Si falla el registro, se muestra un mensaje de error.
        } else {
            $errors[] = "Hubo un problema al registrar al usuario. Inténtalo de nuevo.";
        }
    }
}

// Se carga la vista del formulario de registro personalizado para usuarios de Google.
require __DIR__ . "/../view/printRegisterGoogle.php";
?>
