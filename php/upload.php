<?php
// Include the database connection
include 'dbconnect.php';

session_start();
 echo "Session data: ";
 var_dump($_SESSION);

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    try {
        // Get the audio data from the uploaded file
        $audioData = file_get_contents($_FILES['audio']['tmp_name']);
        $contentType = $_FILES['audio']['type'];

        // Get the user ID from the session or wherever it's stored
        $userID = $_SESSION['user_id']; // Change this based on your actual session variable
        echo "User ID: " . $userID;


        $stmt = $conn->prepare("INSERT INTO audio (userID, data, content_type) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $userID, $audioData, $contentType);

        if ($stmt->execute()) {
            // Query executed successfully
            echo json_encode(['success' => true, 'message' => 'Audio stored successfully']);
        } else {
            // Query execution failed
            echo json_encode(['success' => false, 'message' => 'Error storing audio: ' . $stmt->error]);
        }

        $stmt->close();
        
    } catch (Exception $e) {
        // Handle any errors that occurred during the process
        echo json_encode(['success' => false, 'message' => 'Error storing audio: ' . $e->getMessage()]);
    }
} else {
    // If the form is not submitted, provide an error response
    echo json_encode(['success' => false, 'message' => 'Invalid request']);
}

// Close the database connection
$conn->close();
?>
