<?php
ini_set('display_errors', '1');
ini_set('display_startup_errors', '1');
error_reporting(E_ALL);

//session_start();

$action = $_GET['action'] ?? NULL;

switch ($action) {
    default: 
        require __DIR__ . '/resource_home.php';
        break;
}   
