<?php
$host = 'mysql-db';
$db = 'user_management';
$user = 'root';  // ganti dengan user MySQL Anda
$pass = 'root';      // ganti dengan password MySQL Anda

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>