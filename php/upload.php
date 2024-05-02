<?php

ini_set('max_execution_time', 600);
// Include the database connection
include 'dbconnect.php';

session_start();
echo "Session data: ";
var_dump($_SESSION);

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    try {
        // Check if file path is received
        if (!isset($_POST['filePath'])) {
            throw new Exception('File path not received');
        }

        // Get the file path from the form
        $filePath = $_POST['filePath'];

        // Get the user ID from the session or wherever it's stored
        $userID = $_SESSION['user_id']; // Change this based on your actual session variable
        echo "User ID: " . $userID;

        // Send the path to the Python script
        $pythonScriptPath = '../algorithms/newimplement.py'; // Adjust the path accordingly
        exec("d:/AI/anaconda3/python.exe $pythonScriptPath $filePath ", $output);

        echo "output is: ";
        var_dump($output); // Print the output for debugging

        // Extract individual elements from the output array
        $pitch = $output[0];
        $speakingRate = $output[1];
        $loudness = $output[2];
        $results = $output[3];

        $pythonGraphPath = '../algorithms/graph.py';

        // Execute the Python script and capture the output
        exec("d:/AI/anaconda3/python.exe $pythonGraphPath $filePath", $graph);

        echo "Graph path is";
        var_dump($graph); // Print the output for debugging

        // Extract the graph path from the output
        $graphPath = end($graph); // Assuming the graph path is the last element in the output array

        // Prepare the SQL statement
        $stmt = $conn->prepare("INSERT INTO audio (userID, path, pitch, speakingRate, loudness, results, graphPath) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $stmt->bind_param("sssssss", $userID, $filePath, $pitch, $speakingRate, $loudness, $results, $graphPath);

        // Execute the SQL statement
        if ($stmt->execute()) {
            // Retrieve the auto-generated audio ID
            $audioID = $conn->insert_id;
            // Store the audio ID in the session
            $_SESSION['audioID'] = $audioID;
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
