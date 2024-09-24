<?php
session_start();
if ($_SESSION['role'] != 'user') {
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="flex items-center justify-center h-screen bg-gray-100">
    <div class="text-center">
        <h2 class="text-3xl font-bold">Welcome, Slashroot #8 Player !</h2>
        <p class="text-center mt-6">Sorry, We Not Have Flag !, Please Try Again !</p>
        <p class="mt-4"><a href="logout.php" class="text-blue-500">Logout</a></p>
    </div>
</body>
</html>
