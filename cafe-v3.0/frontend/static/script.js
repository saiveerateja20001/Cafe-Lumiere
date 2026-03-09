// Café Lumière - Customer Order Script

let cart = [];
let currentOrderNumber = null;
let statusCheckInterval = null;

// Switch between categories
function switchCategory(category) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Show selected category
    document.querySelectorAll('.category-grid').forEach(grid => grid.classList.remove('active'));
    document.getElementById(category + '-items').classList.add('active');
}

function addItem(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    
    updateCart();
    updateBadge(id);
    
    // Visual feedback - animate the card
    const card = document.querySelector(`.menu-card[data-item-id="${id}"]`);
    if (card) {
        card.style.animation = 'none';
        setTimeout(() => {
            card.style.animation = 'popIn 0.3s ease';
        }, 10);
    }
}

function updateBadge(itemId) {
    const badge = document.getElementById(`badge-${itemId}`);
    const item = cart.find(i => i.id === itemId);
    
    if (item && item.quantity > 0) {
        badge.textContent = item.quantity;
        badge.classList.add('show');
    } else {
        badge.classList.remove('show');
    }
}

function removeItem(id) {
    cart = cart.filter(item => item.id !== id);
    updateCart();
    updateBadge(id);
}

function updateCart() {
    const cartItemsDiv = document.getElementById('cartItems');
    const totalPriceSpan = document.getElementById('totalPrice');
    
    if (cart.length === 0) {
        cartItemsDiv.innerHTML = '<div style="text-align: center; color: #999; padding: 40px 20px; font-size: 1.1em;"><div style="font-size: 3em; margin-bottom: 10px;">🛒</div><div>Your cart is empty</div></div>';
        totalPriceSpan.textContent = '0.00';
        return;
    }
    
    let html = '';
    let total = 0;
    
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        html += `
            <div class="cart-item">
                <span class="cart-item-name">${item.name}</span>
                <span class="cart-item-quantity">x${item.quantity}</span>
                <span class="cart-item-price">€${itemTotal.toFixed(2)}</span>
                <button class="remove-btn" onclick="removeItem(${item.id})">×</button>
            </div>
        `;
    });
    
    cartItemsDiv.innerHTML = html;
    totalPriceSpan.textContent = total.toFixed(2);
}

async function placeOrder() {
    const customerName = document.getElementById('customerName').value.trim();
    
    if (!customerName) {
        alert('Please enter your name');
        return;
    }
    
    if (cart.length === 0) {
        alert('Please add items to your cart');
        return;
    }
    
    const orderData = {
        customer_name: customerName,
        items: cart,
        total_price: cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    };
    
    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });
        
        if (response.ok) {
            const order = await response.json();
            showOrderConfirmation(order);
        } else {
            alert('Failed to place order. Please try again.');
        }
    } catch (error) {
        console.error('Error placing order:', error);
        alert('Error placing order. Please try again.');
    }
}

function showOrderConfirmation(order) {
    currentOrderNumber = order.order_number;
    
    document.getElementById('orderNumber').textContent = order.order_number;
    document.getElementById('orderCustomer').textContent = order.customer_name;
    
    document.querySelector('.order-section').classList.add('hidden');
    document.getElementById('orderConfirmation').classList.remove('hidden');
    
    updateOrderStatus(order.status);
    
    // Start polling for status updates
    statusCheckInterval = setInterval(checkOrderStatus, 3000);
}

async function checkOrderStatus() {
    if (!currentOrderNumber) return;
    
    try {
        const response = await fetch(`/api/orders/${currentOrderNumber}`);
        if (response.ok) {
            const order = await response.json();
            updateOrderStatus(order.status);
            
            if (order.status === 'served') {
                clearInterval(statusCheckInterval);
            }
        }
    } catch (error) {
        console.error('Error checking order status:', error);
    }
}

function updateOrderStatus(status) {
    const statuses = ['ordered', 'preparing', 'ready', 'served'];
    const currentIndex = statuses.indexOf(status);
    
    statuses.forEach((s, index) => {
        const element = document.getElementById(`status${s.charAt(0).toUpperCase() + s.slice(1)}`);
        if (index <= currentIndex) {
            element.classList.add('active');
        } else {
            element.classList.remove('active');
        }
    });
}

function newOrder() {
    clearInterval(statusCheckInterval);
    currentOrderNumber = null;
    cart = [];
    
    document.getElementById('customerName').value = '';
    updateCart();
    
    document.getElementById('orderConfirmation').classList.add('hidden');
    document.querySelector('.order-section').classList.remove('hidden');
    
    // Reset status indicators
    ['ordered', 'preparing', 'ready', 'served'].forEach(status => {
        document.getElementById(`status${status.charAt(0).toUpperCase() + status.slice(1)}`).classList.remove('active');
    });
}

// Initialize
updateCart();
