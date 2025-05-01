<?php

if (!isset($_SESSION['id_user'])) {
    header("Location: index.php?action=resource-login");
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_once __DIR__ . "/../model/connectDB.php";
    require_once __DIR__ . "/../model/checkUpdateUserInfo.php";

    $userId = $_SESSION['id_user'];
    $password = $_POST['password'];
    $confirmPassword = $_POST['confirm_password'];

    if ($password === $confirmPassword) {
        $connection = connectDB();
        $result = updatePassword($connection, $userId, $password);

        if ($result) {
            header("Location: index.php?action=resource-myAccount&success=password");
            exit();
        }
    }
}

header("Location: index.php?action=resource-myAccount");
exit();

?>
