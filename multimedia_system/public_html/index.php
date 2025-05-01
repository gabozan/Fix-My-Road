<?php
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

//session_start();

$action = $_GET['action'] ?? NULL;

switch ($action) {
    case 'resource-register':
        require __DIR__ . '/resource_register.php';
        break;
    case 'resource-login':
        require __DIR__ . '/resource_login.php';
        break;
    case 'update-user-info':
        require __DIR__ . '/controller/controllerUpdateUserInfo.php';
        break;
    case 'resource-myAccount':
        require __DIR__ . '/resource_myAccount.php';
        break;
    case 'logout':
        require __DIR__ . '/controller/controllerLogout.php';
        break;
    default: 
        require __DIR__ . '/resource_home.php';
        break;
}   
