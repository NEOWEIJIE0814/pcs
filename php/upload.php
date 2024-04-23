<?php
// Include the database connection
include 'dbconnect.php';

session_start();
echo "Session data: ";
var_dump($_SESSION);

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    try {
        // Check if file is uploaded
        if (!isset($_FILES['audio']) || $_FILES['audio']['error'] !== UPLOAD_ERR_OK) {
            throw new Exception('Error uploading audio file');
        }

        // Get the audio data from the uploaded file
        $audioData = file_get_contents($_FILES['audio']['tmp_name']);
        $contentType = $_FILES['audio']['type'];

        // Get the user ID from the session or wherever it's stored
        $userID = $_SESSION['user_id']; // Change this based on your actual session variable
        echo "User ID: " . $userID;

        // Write the audio data to a temporary file
        $tempAudioFile = tempnam(sys_get_temp_dir(), 'audio_');
        file_put_contents($tempAudioFile, $_FILES['audio']);

        // Send the path of the temporary audio file to the Python script
        $pythonScriptPath = '../algorithms/implement.py'; // Adjust the path accordingly
        $output = '';
        exec("python $pythonScriptPath '$tempAudioFile' 2>&1", $output);
        $output = trim(implode("\n", $output));

        // Prepare the SQL statement
        $stmt = $conn->prepare("INSERT INTO audio (userID, data, content_type, results) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("ssss", $userID, $audioData, $contentType, $output);

        // Execute the SQL statement
        if ($stmt->execute()) {
            // Query executed successfully
            echo json_encode(['success' => true, 'message' => 'Audio stored successfully']);
        } else {
            // Query execution failed
            throw new Exception('Error storing audio: ' . $stmt->error);
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