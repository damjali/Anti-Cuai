/**
 * content.js
 * This script runs in the context of the web page but cannot 
 * directly call local APIs due to Private Network Access restrictions.
 */

(function() {
    // 1. Identify the URL or data you want to check
    const currentUrl = window.location.href;

    console.log("Anti-Cuai content script active. Checking:", currentUrl);

    // 2. Send a message to the background.js service worker
    // Instead of fetching directly, we ask the extension background to do it.
    chrome.runtime.sendMessage(
        { 
            action: "checkPhishing", 
            url: currentUrl 
        }, 
        (response) => {
            // Check for connection errors between content and background
            if (chrome.runtime.lastError) {
                console.error("Anti-Cuai communication error:", chrome.runtime.lastError.message);
                return;
            }

            // 3. Handle the response sent back from background.js
            if (response && response.success) {
                handleApiResponse(response.data);
            } else {
                console.error("Anti-Cuai backend error:", response.error);
            }
        }
    );
})();

/**
 * Handle the UI logic based on the API verdict
 */
function handleApiResponse(data) {
    console.log("Anti-Cuai Verdict Received:", data);
    
    // Example logic: if the API returns that it's phishing, alert the user
    if (data.is_phishing || data.status === "suspicious") {
        alert("⚠️ WARNING: Anti-Cuai has detected this site as potentially unsafe!");
        
        // You could also inject a warning banner into the DOM here
        const banner = document.createElement('div');
        banner.style.cssText = "position:fixed; top:0; left:0; width:100%; background:red; color:white; text-align:center; z-index:9999; padding:10px; font-weight:bold;";
        banner.innerText = "SECURITY WARNING: This site is flagged as a phishing risk.";
        document.body.prepend(banner);
    }
}