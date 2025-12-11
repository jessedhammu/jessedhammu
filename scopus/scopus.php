<?php

// Your SCOPUS API Key
$apiKey = 'eb8a60c6ef39e29de535e53fc695103e';

// SCOPUS API endpoint for searching documents
$url = 'https://api.elsevier.com/content/search/scopus';

// Define your query parameters (customize as per your institution's requirements)
$queryParams = [
    'query' => 'AF-ID("Central University of Punjab" 60106790)', // Replace with your institution's name
    'count' => 25, // Fetch 25 documents per batch
    'start' => 0, // Start from the first document
];

// Set up HTTP headers with the API key
$headers = [
    "X-ELS-APIKey: $apiKey",
    "Accept: application/json"
];

// Initialize variables
$totalDocuments = 0;
$totalCitations = 0;
$citationsArray = [];

// Initialize cURL
$ch = curl_init();

do {
    // Build the URL with query parameters
    $queryString = http_build_query($queryParams);
    $batchUrl = $url . '?' . $queryString;

    // Set cURL options
    curl_setopt($ch, CURLOPT_URL, $batchUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    // Execute the request and capture the response
    $response = curl_exec($ch);

    // Check for errors
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        break;
    }

    // Decode the JSON response
    $data = json_decode($response, true);

    // Extract total document count from the first batch
    if ($totalDocuments === 0 && isset($data['search-results']['opensearch:totalResults'])) {
        $totalDocuments = (int)$data['search-results']['opensearch:totalResults'];
    }

// Store unique documents using their EID
$uniqueDocuments = [];

if (isset($data['search-results']['entry'])) {
    foreach ($data['search-results']['entry'] as $entry) {
        // Extract EID (unique document identifier)
        $eid = $entry['eid'] ?? null;

        // Only count the document if its EID is not already processed
        if ($eid && !isset($uniqueDocuments[$eid])) {
            $uniqueDocuments[$eid] = true; // Mark EID as processed
            $citationsArray[] = (int)($entry['citedby-count'] ?? 0); // Add to citations array
            $totalCitations += (int)($entry['citedby-count'] ?? 0); // Add to total citations
        }
    }
}

    // Increment the starting point for the next batch
    $queryParams['start'] += $queryParams['count'];

} while (!empty($data['search-results']['entry']));

// Close cURL
curl_close($ch);

// Calculate the h-index
sort($citationsArray, SORT_NUMERIC); // Sort citations in ascending order
$hIndex = 0;
$citationsArray = array_reverse($citationsArray); // Reverse to descending order
foreach ($citationsArray as $index => $citationCount) {
    if ($citationCount >= $index + 1) {
        $hIndex = $index + 1;
    } else {
        break;
    }
}

// Get the current date
$currentDate = date('d-m-Y');

// Print results
echo "Date: $currentDate\n";
echo "Institution: Central University of Punjab\n";
echo "Total Documents: $totalDocuments\n";
echo "Total Citations: $totalCitations\n";
echo "h-Index: $hIndex\n";

// Write the results to a CSV file
$csvFilePath = '/var/www/html/scopus_data.csv';

// Check if the file exists, create headers if not
if (!file_exists($csvFilePath)) {
    $headers = ['Date', 'Total Documents', 'Total Citations', 'h-Index'];
    $file = fopen($csvFilePath, 'w');
    fputcsv($file, $headers);
    fclose($file);
}

// Append the data
$file = fopen($csvFilePath, 'a');
$row = [$currentDate, $totalDocuments, $totalCitations, $hIndex];
fputcsv($file, $row);
fclose($file);

echo "Data has been written to $csvFilePath.\n";

?>
