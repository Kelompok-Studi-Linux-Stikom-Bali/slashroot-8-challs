<?php
$host = 'localhost';
$db = 'user_management';
$user = 'Slashroot8_ctf';  // ganti dengan user MySQL Anda
$pass = 'fH*5)sng.0eOT*KC';      // ganti dengan password MySQL Anda

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>