// Café Lumière - Kitchen Management Script

let orders = [];

async function loadKitchenOrders() {
    try {
        const response = await fetch('/api/kitchen/orders');
        if (response.ok) {
            orders = await response.json();
            displayOrders();
        }
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

function displayOrders() {
    const orderedDiv = document.getElementById('orderedOrders');
    const preparingDiv = document.getElementById('preparingOrders');
    const readyDiv = document.getElementById('readyOrders');
    
    orderedDiv.innerHTML = '';
    preparingDiv.innerHTML = '';
    readyDiv.innerHTML = '';
    
    orders.forEach(order => {
        const card = createOrderCard(order);
        
        if (order.status === 'ordered') {
            orderedDiv.appendChild(card);
        } else if (order.status === 'preparing') {
            preparingDiv.appendChild(card);
        } else if (order.status === 'ready') {
            readyDiv.appendChild(card);
        }
    });
    
    if (orderedDiv.children.length === 0) {
        orderedDiv.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">No new orders</p>';
    }
    if (preparingDiv.children.length === 0) {
        preparingDiv.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">Nothing preparing</p>';
    }
    if (readyDiv.children.length === 0) {
        readyDiv.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">No orders ready</p>';
    }
}

function createOrderCard(order) {
    const card = document.createElement('div');
    card.className = `order-card ${order.status}`;
    
    const time = new Date(order.created_at).toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const items = typeof order.items === 'string' ? JSON.parse(order.items) : order.items;
    const itemsList = items.map(item => `<li>${item.name} x${item.quantity}</li>`).join('');
    
    let actions = '';
    if (order.status === 'ordered') {
        actions = `<button class="action-btn start-btn" onclick="startPreparing('${order.order_number}')">Start Preparing</button>`;
    } else if (order.status === 'preparing') {
        actions = `<button class="action-btn ready-btn" onclick="markReady('${order.order_number}')">Mark Ready</button>`;
    } else if (order.status === 'ready') {
        actions = `<button class="action-btn serve-btn" onclick="serveOrder('${order.order_number}')">Serve Order</button>`;
    }
    
    card.innerHTML = `
        <div class="order-header">
            <span class="order-number">${order.order_number}</span>
            <span class="order-time">${time}</span>
        </div>
        <div class="order-customer">👤 ${order.customer_name}</div>
        <ul class="order-items">${itemsList}</ul>
        <div style="text-align: right; font-weight: bold; color: var(--primary); margin-top: 10px;">
            Total: €${parseFloat(order.total_price).toFixed(2)}
        </div>
        <div class="order-actions">${actions}</div>
    `;
    
    return card;
}

async function startPreparing(orderNumber) {
    try {
        const response = await fetch(`/api/kitchen/orders/${orderNumber}/start`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadKitchenOrders();
        } else {
            alert('Failed to update order status');
        }
    } catch (error) {
        console.error('Error starting order:', error);
        alert('Error updating order');
    }
}

async function markReady(orderNumber) {
    try {
        const response = await fetch(`/api/kitchen/orders/${orderNumber}/ready`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadKitchenOrders();
        } else {
            alert('Failed to update order status');
        }
    } catch (error) {
        console.error('Error marking order ready:', error);
        alert('Error updating order');
    }
}

async function serveOrder(orderNumber) {
    try {
        const response = await fetch(`/api/kitchen/orders/${orderNumber}/serve`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadKitchenOrders();
        } else {
            alert('Failed to update order status');
        }
    } catch (error) {
        console.error('Error serving order:', error);
        alert('Error updating order');
    }
}

// Auto-refresh every 5 seconds
setInterval(loadKitchenOrders, 5000);

// Initial load
loadKitchenOrders();
