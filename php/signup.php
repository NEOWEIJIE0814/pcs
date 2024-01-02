<?php
include 'dbconnect.php';

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Get the values from the form
    $username = $_POST["username"];
    $email = $_POST["email"];
    $password = $_POST["password"];
    $name = $_POST["name"];
    $age = $_POST["age"];
    $gender = $_POST["gender"];

    // Prepare and bind the SQL statement
    $stmt = $conn->prepare("INSERT INTO users (username, email, password, name, age, gender) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("sssssi", $username, $email, $password, $name, $age, $gender);

    // Execute the statement
    if ($stmt->execute()) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $stmt->error;
    }

    // Close the statement
    $stmt->close();
}

// Close the connection
$conn->close();
?>