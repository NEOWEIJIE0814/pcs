<?php

// Include your database connection file
include("dbconnect.php");

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $full_name = mysqli_real_escape_string($conn, $_POST["full_name"]);
    $username = mysqli_real_escape_string($conn, $_POST["username"]);
    $email = mysqli_real_escape_string($conn, $_POST["email"]);
    $age = intval($_POST["age"]);
    $gender = mysqli_real_escape_string($conn, $_POST["gender"]);
    $password = password_hash($_POST["password"], PASSWORD_DEFAULT); // Hash the password

    // Check if the email is already registered
    $check_email_query = "SELECT * FROM users WHERE email='$email'";
    $email_result = mysqli_query($conn, $check_email_query);

    // Check if the username is already registered
    $check_username_query = "SELECT * FROM users WHERE username='$username'";
    $username_result = mysqli_query($conn, $check_username_query);

    if (mysqli_num_rows($email_result) > 0 && mysqli_num_rows($username_result) > 0) {
        echo "<script>
            alert('Email and username are already registered!');
            window.history.back();
        </script>";
    } elseif (mysqli_num_rows($email_result) > 0) {
        echo "<script>
            alert('Email is already registered!');
            window.history.back();
        </script>";
    } elseif (mysqli_num_rows($username_result) > 0) {
        echo "<script>
            alert('Username is already registered!');
            window.history.back();
        </script>";
    } else {
        // Insert data into the "users" table
        $query = "INSERT INTO users (full_name, username, email, age, gender, password) VALUES ('$full_name', '$username', '$email', $age, '$gender', '$password')";

        if (mysqli_query($conn, $query)) {
            echo "<script>
                alert('Registration successful!');
                window.location.href = '../page/login.html';
            </script>";
        } else {
            echo "Error: " . $query . "<br>" . mysqli_error($conn);
        }
    }

    // Close the database connection
    mysqli_close($conn);
}

?>
