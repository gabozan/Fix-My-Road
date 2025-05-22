<?php
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

session_start();

$action = $_GET['action'] ?? NULL;

switch ($action) {
    case 'resource-howWeAre':
        require __DIR__ . '/resource_howWeAre.php';
        break;
    case 'resource-faq':
        require __DIR__ . '/resource_faq.php';
        break;
    case 'resource_login_google':
        require __DIR__ . '/controller/controllerLoginGoogle.php';
        break;
    case 'resource_register_google':
        require __DIR__ . '/resource_register_google.php';
        break;
    case 'resource-image-detect':
        require __DIR__ . '/resource_image_detect.php';
        break;
    case 'resource-video-detect':
        require __DIR__ . '/resource_video_detect.php';
        break;
    case 'resource-real-time':
        require __DIR__ . '/resource_real_time.php';
        break;
    case 'resource-ranking':
        require __DIR__ . '/resource_ranking.php';
        break;
    case 'resource-register':
        require __DIR__ . '/resource_register.php';
        break;
    case 'resource-login':
        require __DIR__ . '/resource_login.php';
        break;
    case 'update-user-info':
        require __DIR__ . '/controller/controllerUpdateUserInfo.php';
        break;        
    case 'update-pass-info':
        require __DIR__ . '/controller/controllerUpdatePassInfo.php';
        break;
    case 'resource-myAccount':
        require __DIR__ . '/resource_myAccount.php';
        break;
    case 'logout':
        require __DIR__ . '/controller/controllerLogout.php';
        break;
    case 'get-damages':
        require __DIR__ . '/controller/controllerGetDamages.php';
        break;
    default: 
        require __DIR__ . '/resource_home.php';
        break;
}   
