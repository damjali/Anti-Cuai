// background.js

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // Check if the message is asking to check for phishing
    if (request.action === "checkPhishing") {
        
        console.log("Background received URL to check:", request.url);

        // Perform the fetch here, safely away from the webpage's strict security policies
        fetch('http://127.0.0.1:8000/api/check/phishing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: request.url })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Send the API's verdict back to the content script
            sendResponse({ success: true, data: data });
        })
        .catch(error => {
            console.error("Anti-Cuai Background Fetch Error:", error);
            sendResponse({ success: false, error: error.message });
        });

        // CRITICAL: Return true to keep the message channel open for the async fetch
        return true; 
    }
});