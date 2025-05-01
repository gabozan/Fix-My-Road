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
    $password = $_POST['password'];
    $confirmPassword = $_POST['confirm_password'];

    if ($password == $confirmPassword) {
        if (isset($_FILES['profile_picture']) && !empty($_FILES['profile_picture'])) {
            if ($_FILES['profile_picture']['name'] !== 'default_profile_picture.png') {
                $baseName = pathinfo($_FILES['profile_picture']['name'], PATHINFO_FILENAME);
                $cleanBaseName = preg_replace('/[^a-zA-Z0-9-_]/', '', $baseName);
                $fileExtension = pathinfo($_FILES['profile_picture']['name'], PATHINFO_EXTENSION);
                $uniqueFileName = $cleanBaseName . "_user_" . $userId . "." . $fileExtension;
                $destinationPath = $filesAbsolutePath . $uniqueFileName;
                move_uploaded_file($_FILES['profile_picture']['tmp_name'], $destinationPath);
            } else {
                $uniqueFileName = NULL;
            }
        } else {
            $uniqueFileName = NULL;
        }

        $connection = connectDB();
        $result = updateUser($connection, $userId, $email, $password, $name, $uniqueFileName);

        if ($result) {
            $_SESSION["user_email"] = $email;
            header("Location: index.php");
            exit();
        }
    }
}

header("Location: index.php?action=resource-myAccount");
exit();

?>
