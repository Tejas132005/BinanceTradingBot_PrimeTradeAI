/**
 * Binance Futures Testnet Trading Bot - Frontend Logic
 * Handles dynamic UI updates, form validation, and asynchronous order submission.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Form Elements
    const orderForm = document.getElementById("orderForm");
    const symbolInput = document.getElementById("symbol");
    const sideSelect = document.getElementById("side");
    const orderTypeSelect = document.getElementById("order_type");
    const quantityInput = document.getElementById("quantity");
    const priceGroup = document.getElementById("priceGroup");
    const priceInput = document.getElementById("price");
    const stopPriceGroup = document.getElementById("stopPriceGroup");
    const stopPriceInput = document.getElementById("stop_price");
    
    // Submit Button Elements
    const submitBtn = document.getElementById("submitBtn");
    const submitBtnText = document.getElementById("submitBtnText");
    const submitSpinner = document.getElementById("submitSpinner");
    const submitIcon = document.getElementById("submitIcon");
    
    // Alert & Terminal Elements
    const formAlert = document.getElementById("formAlert");
    const terminalOutput = document.getElementById("terminalOutput");
    const lastActionTime = document.getElementById("lastActionTime");

    /**
     * Updates UI state based on selected Order Type and Side.
     */
    function updateUIState() {
        const orderType = orderTypeSelect.value;
        const side = sideSelect.value;

        // 1. Show/Hide Price and Stop Price Fields
        if (orderType === "MARKET") {
            priceGroup.classList.add("d-none");
            priceInput.required = false;
            stopPriceGroup.classList.add("d-none");
            stopPriceInput.required = false;
        } else if (orderType === "LIMIT") {
            priceGroup.classList.remove("d-none");
            priceInput.required = true;
            stopPriceGroup.classList.add("d-none");
            stopPriceInput.required = false;
        } else if (orderType === "STOP") {
            priceGroup.classList.remove("d-none");
            priceInput.required = true;
            stopPriceGroup.classList.remove("d-none");
            stopPriceInput.required = true;
        }

        // 2. Update Submit Button Styling and Label
        const typeLabel = orderType === "STOP" ? "Stop-Limit" : orderType.charAt(0).toUpperCase() + orderType.slice(1).toLowerCase();
        const sideLabel = side === "BUY" ? "Buy" : "Sell";
        submitBtnText.textContent = `Execute ${typeLabel} ${sideLabel}`;

        if (side === "SELL") {
            submitBtn.classList.add("btn-sell");
        } else {
            submitBtn.classList.remove("btn-sell");
        }
    }

    /**
     * Displays Bootstrap alert message.
     */
    function showAlert(message, isSuccess = true) {
        formAlert.className = `alert alert-${isSuccess ? 'success' : 'danger'} mb-4`;
        formAlert.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fa-solid ${isSuccess ? 'fa-circle-check text-success' : 'fa-triangle-exclamation text-danger'} me-2 fs-5"></i>
                <div>${message}</div>
            </div>
        `;
        formAlert.classList.remove("d-none");
    }

    /**
     * Appends text to the Execution Terminal.
     */
    function appendToTerminal(text, isError = false) {
        const welcomeMsg = document.querySelector(".terminal-welcome");
        if (welcomeMsg) welcomeMsg.classList.add("d-none");

        terminalOutput.classList.remove("d-none");
        
        // Format timestamp
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        
        lastActionTime.textContent = `Last update: ${timeStr}`;

        // Ensure proper color styling in terminal
        let colorClass = isError ? "text-danger" : "text-light";
        if (!isError && text.includes("SUCCESS")) {
            colorClass = "text-success";
        }

        terminalOutput.innerHTML = `<span class="${colorClass}">${text}</span>`;
    }

    // Event Listeners for Dynamic UI updates
    sideSelect.addEventListener("change", updateUIState);
    orderTypeSelect.addEventListener("change", updateUIState);

    // Initial UI setup
    updateUIState();

    /**
     * Handle Order Form Submission
     */
    orderForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        // Hide previous alerts
        formAlert.classList.add("d-none");

        // Basic HTML5 Form Validation check
        if (!orderForm.checkValidity()) {
            orderForm.classList.add("was-validated");
            showAlert("Validation Error: Please fill in all required fields correctly.", false);
            appendToTerminal("[VALIDATION ERROR] Required form fields are missing or invalid.\n\nTip: If Limit or Stop-Limit is selected, ensure Price and Stop Price fields are correctly filled with positive numbers.", true);
            return;
        }

        // Prepare payload
        const payload = {
            symbol: symbolInput.value.trim().toUpperCase(),
            side: sideSelect.value,
            order_type: orderTypeSelect.value,
            quantity: quantityInput.value.trim(),
            price: orderTypeSelect.value !== "MARKET" ? priceInput.value.trim() : null,
            stop_price: orderTypeSelect.value === "STOP" ? stopPriceInput.value.trim() : null
        };

        // UI Loading State
        submitBtn.disabled = true;
        submitSpinner.classList.remove("d-none");
        submitIcon.classList.add("d-none");
        submitBtnText.textContent = "Processing Order...";

        try {
            appendToTerminal(`[${new Date().toLocaleTimeString()}] Sending order request to backend...`);
            
            const response = await fetch("/place-order", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.ok && result.success) {
                showAlert(result.message, true);
                appendToTerminal(result.formatted_summary, false);
            } else {
                showAlert(result.message || "Failed to execute order.", false);
                appendToTerminal(`[ERROR] ${result.message || "Execution Failed"}\nError Type: ${result.error_type || "Unknown"}`, true);
            }

        } catch (error) {
            console.error("Order submission error:", error);
            showAlert("Network error: Unable to connect to the trading bot backend.", false);
            appendToTerminal(`[CRITICAL ERROR] Network connection failure.\nDetails: ${error.message}`, true);
        } finally {
            // Restore UI State
            submitBtn.disabled = false;
            submitSpinner.classList.add("d-none");
            submitIcon.classList.remove("d-none");
            updateUIState();
        }
    });
});

/**
 * Clears the terminal display.
 */
function clearTerminal() {
    const terminalOutput = document.getElementById("terminalOutput");
    const welcomeMsg = document.querySelector(".terminal-welcome");
    const lastActionTime = document.getElementById("lastActionTime");

    terminalOutput.innerHTML = "";
    terminalOutput.classList.add("d-none");
    if (welcomeMsg) welcomeMsg.classList.remove("d-none");
    lastActionTime.textContent = "Status: Terminal cleared.";
}
