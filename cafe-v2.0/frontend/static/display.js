// Café Lumière - Display Board Script

async function loadDisplayOrders() {
    try {
        const response = await fetch('/api/display/orders');
        if (response.ok) {
            const orders = await response.json();
            displayReadyOrders(orders.filter(o => o.status === 'ready'));
            displayPreparingOrders(orders.filter(o => o.status === 'preparing'));
            clearErrorMessage();
        } else {
            showErrorMessage(`Error: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        showErrorMessage(`Connection error: Unable to load orders`);
    }
}

function displayReadyOrders(orders) {
    const readyDiv = document.getElementById('readyDisplay');
    
    if (orders.length === 0) {
        readyDiv.innerHTML = '<p style="text-align: center; color: #999; padding: 40px; font-size: 1.1em;">No orders ready</p>';
        return;
    }
    
    readyDiv.innerHTML = orders.map(order => `
        <div class="display-card ready-card">
            <div class="display-order-number">${order.order_number}</div>
            <div class="display-customer">${order.customer_name}</div>
            <div style="font-size: 2em; margin-top: 10px;">✅ Ready!</div>
        </div>
    `).join('');
}

function displayPreparingOrders(orders) {
    const preparingDiv = document.getElementById('preparingDisplay');
    
    if (orders.length === 0) {
        preparingDiv.innerHTML = '<p style="text-align: center; color: #999; padding: 40px; font-size: 1.1em;">No orders being prepared</p>';
        return;
    }
    
    preparingDiv.innerHTML = orders.map(order => `
        <div class="display-card preparing-card">
            <div class="display-order-number">${order.order_number}</div>
            <div class="display-customer">${order.customer_name}</div>
            <div style="font-size: 1.8em; margin-top: 10px; color: var(--preparing);">👨‍🍳 Preparing...</div>
        </div>
    `).join('');
}

function showErrorMessage(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
}

function clearErrorMessage() {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

// Auto-refresh every 3 seconds
setInterval(loadDisplayOrders, 3000);

// Initial load
loadDisplayOrders();

// Add pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`;
document.head.appendChild(style);
