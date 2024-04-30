<?php
// Include the database connection
include 'dbconnect.php';

// Start the session
session_start();

// Check if the audio ID is stored in the session
if (!isset($_SESSION['audioID'])) {
    echo json_encode(['success' => false, 'message' => 'Audio ID not found in session']);
    exit; // Terminate the script
}

// Get the audio ID from the session
$audioID = $_SESSION['audioID'];

// Query to retrieve audio information from the database
$query = "SELECT * FROM audio WHERE audioID = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("i", $audioID);

// Execute the query
if ($stmt->execute()) {
    // Fetch the result
    $result = $stmt->get_result();

    // Check if any rows are returned
    if ($result->num_rows > 0) {
        // Fetch the audio data
        $audioData = $result->fetch_assoc();
        
        // Return the audio data as JSON
        echo json_encode(['success' => true, 'audio' => $audioData]);
    } else {
        echo json_encode(['success' => false, 'message' => 'No audio data found']);
    }
} else {
    // Log the database error
    error_log("Error executing query: " . $conn->error);
    echo json_encode(['success' => false, 'message' => 'Database error']);
}

// Close the database connection
$stmt->close();
$conn->close();
?>
