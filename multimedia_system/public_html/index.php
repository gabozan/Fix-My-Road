<?php
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

$action = $_GET['action'] ?? NULL;

switch ($action) {
    case 'home':
        include 'home.php';
        break;
    default: 
        require __DIR__ . '/resource_home.php';
        break;
}   
