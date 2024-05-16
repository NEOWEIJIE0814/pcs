<?php

session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Include your database connection file
    include("dbconnect.php"); // Update this with your actual database connection script

    // Get the input values
    $username_email = mysqli_real_escape_string($conn, $_POST["username_email"]);
    $password = $_POST["password"];

    // Check if the input is a valid email address
    if (filter_var($username_email, FILTER_VALIDATE_EMAIL)) {
        $sql = "SELECT * FROM users WHERE email='$username_email'";
    } else {
        $sql = "SELECT * FROM users WHERE username='$username_email'";
    }

    $result = mysqli_query($conn, $sql);

    if ($result) {
        if ($row = mysqli_fetch_assoc($result)) {
            // Verify the password
            if (password_verify($password, $row["password"])) {
                // Password is correct, set session variables and redirect
                $_SESSION["user_id"] = $row["userID"];
                $_SESSION["username"] = $row["username"];
                header("Location: ../page/main.html"); // Redirect to your main page
                exit();
            } else {
                // Password is incorrect
                header("Location: ../page/login.html?error=" . urlencode("Invalid password. Please try again."));
                exit();
            }
        } else {
            // No user found with the provided username or email
            header("Location: ../page/login.html?error=" . urlencode("Invalid username or email. Please try again."));
            exit();
        }
    } else {
        // Error in the SQL query
        header("Location: ../page/login.html?error=" . urlencode("Error: " . mysqli_error($conn)));
        exit();
    }

    // Close the database connection
    mysqli_close($conn);
}

?>
