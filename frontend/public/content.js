// public/content.js

console.log("🛡️ Anti-Cuai Content Script is running!");

// Simple regex to find Malaysian phone numbers (e.g., 012-3456789 or 0123456789)
const phoneRegex = /(01\d{1}-?\d{7,8})/g;

// Function to scan the webpage text
function scanPageForNumbers() {
    // Get all text on the website
    const bodyText = document.body.innerHTML;
    
    // Check if there are phone numbers
    const foundNumbers = bodyText.match(phoneRegex);
    
    if (foundNumbers) {
        // Remove duplicates
        const uniqueNumbers = [...new Set(foundNumbers)];
        console.log("Found numbers to check:", uniqueNumbers);
        
        // Loop through each number and send it to your backend
        uniqueNumbers.forEach(number => {
            checkNumberWithBackend(number);
        });
    }
}

// Function to talk to Hazim/Adam's FastAPI (Assume it runs on localhost:8000 for now)
async function checkNumberWithBackend(number) {
    try {
        // Replace with actual FastAPI endpoint later
        const response = await fetch('http://127.0.0.1:8000/check-scam', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone_number: number })
        });
        
        const data = await response.json();
        
        // If the backend says it's a scam, pass the number AND the report count to the UI
        if (data.is_scam) {
            highlightScamOnPage(number, data.report_count);
        }
    } catch (error) {
        console.error("Failed to connect to backend", error);
    }
}

// The visually cool part: Injecting the warning next to the number
function highlightScamOnPage(scamNumber, reportCount) {
    // Find where the number is on the page
    const regex = new RegExp(scamNumber, 'g');
    
    // We create a custom HTML badge that replaces the plain text number
    // This adds the highly visible red pill showing the total police reports
    const warningHTML = `
        <span style="background-color: #ffe6e6; border: 1px dashed #cc0000; padding: 2px 6px; border-radius: 4px; color: #cc0000; font-weight: bold; display: inline-flex; align-items: center; gap: 4px;">
            🚨 ${scamNumber} 
            <span style="background-color: #cc0000; color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; margin-left: 4px; box-shadow: 0 2px 4px rgba(204,0,0,0.4);">
                ${reportCount} Police Reports!
            </span>
        </span>
    `;
    
    // Inject the badge into the website's DOM
    document.body.innerHTML = document.body.innerHTML.replace(regex, warningHTML);
}

// Run the scan 2 seconds after the page loads to give the website time to render
setTimeout(scanPageForNumbers, 2000);