// ============================================
// MENZA - Frontend Application
// ============================================

// API URL - koristi relativan path kad je na istom originu
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000/api/v1'
    : '/api/v1';

// State
let cart = [];
let menuItems = [];
let currentUser = null;
let token = null;

// ============ INITIALIZATION ============

document.addEventListener('DOMContentLoaded', () => {
    // Load saved auth
    token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateAuthUI();
    }
    
    // Load menu
    loadMenu();
    
    // Load cart from localStorage
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartUI();
    }
    
    // Setup navigation
    setupNavigation();
    
    // Setup hamburger menu
    setupHamburgerMenu();
    
    // Set default pickup time (2 hours from now)
    setDefaultPickupTime();
});

// ============ HAMBURGER MENU ============

function setupHamburgerMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (!hamburger || !mobileMenu) return;
    
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });
    
    // Close menu when clicking a link
    mobileMenu.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
    
    // Mobile login button
    const mobileLoginBtn = document.getElementById('mobileLoginBtn');
    if (mobileLoginBtn) {
        mobileLoginBtn.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
            showLogin();
        });
    }
    
    // Mobile logout button
    const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
    if (mobileLogoutBtn) {
        mobileLogoutBtn.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileMenu.classList.remove('active');
            document.body.style.overflow = '';
            logout();
        });
    }
}

function setupNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            showSection(section);
            
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    const section = document.getElementById(`${sectionName}-section`);
    if (section) {
        section.classList.add('active');
    }
    
    // Load data for specific sections
    if (sectionName === 'orders' && currentUser) {
        loadMyOrders();
    }
}

// ============ AUTH ============

function showLogin() {
    closeModal('register-modal');
    document.getElementById('login-modal').classList.add('active');
    document.getElementById('login-error').textContent = '';
}

function showRegister() {
    closeModal('login-modal');
    document.getElementById('register-modal').classList.add('active');
    document.getElementById('register-error').textContent = '';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');
    
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Greška pri prijavi');
        }
        
        const data = await response.json();
        token = data.access_token;
        localStorage.setItem('token', token);
        
        // Get user info
        await fetchCurrentUser();
        
        closeModal('login-modal');
        showToast('Uspješna prijava!', 'success');
        
        // Refresh orders if on that section
        if (document.getElementById('orders-section').classList.contains('active')) {
            loadMyOrders();
        }
        
    } catch (error) {
        errorEl.textContent = error.message;
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const fullName = document.getElementById('register-fullname').value;
    const password = document.getElementById('register-password').value;
    const errorEl = document.getElementById('register-error');
    
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username,
                email,
                full_name: fullName || null,
                password
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Greška pri registraciji');
        }
        
        closeModal('register-modal');
        showToast('Uspješna registracija! Sada se prijavi.', 'success');
        showLogin();
        
    } catch (error) {
        errorEl.textContent = error.message;
    }
}

async function fetchCurrentUser() {
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            localStorage.setItem('user', JSON.stringify(currentUser));
            updateAuthUI();
        }
    } catch (error) {
        console.error('Error fetching user:', error);
    }
}

function updateAuthUI() {
    const authEl = document.getElementById('nav-auth');
    const userEl = document.getElementById('nav-user');
    const userNameEl = document.getElementById('user-name');
    const adminLink = document.getElementById('admin-link');
    
    // Mobile elements
    const mobileLoginBtn = document.getElementById('mobileLoginBtn');
    const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
    const mobileAdminLink = document.getElementById('mobileAdminLink');
    
    if (currentUser) {
        if (authEl) authEl.style.display = 'none';
        if (userEl) userEl.style.display = 'flex';
        if (userNameEl) userNameEl.textContent = currentUser.full_name || currentUser.username;
        
        if (currentUser.role === 'admin') {
            if (adminLink) adminLink.style.display = 'inline-flex';
            if (mobileAdminLink) mobileAdminLink.style.display = 'inline-flex';
        }
        
        // Mobile
        if (mobileLoginBtn) mobileLoginBtn.style.display = 'none';
        if (mobileLogoutBtn) mobileLogoutBtn.style.display = 'inline-flex';
    } else {
        if (authEl) authEl.style.display = 'flex';
        if (userEl) userEl.style.display = 'none';
        if (adminLink) adminLink.style.display = 'none';
        
        // Mobile
        if (mobileLoginBtn) mobileLoginBtn.style.display = 'inline-flex';
        if (mobileLogoutBtn) mobileLogoutBtn.style.display = 'none';
        if (mobileAdminLink) mobileAdminLink.style.display = 'none';
    }
}

function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    updateAuthUI();
    showToast('Odjavljen/a', 'success');
    
    // Redirect to home if on admin page
    if (window.location.pathname.includes('admin')) {
        window.location.href = '/';
    }
}

// ============ MENU ============

async function loadMenu() {
    try {
        const response = await fetch(`${API_URL}/menu/?available_only=false`);
        menuItems = await response.json();
        renderMenu(menuItems);
        renderCategoryFilters();
    } catch (error) {
        console.error('Error loading menu:', error);
        showToast('Greška pri učitavanju jelovnika', 'error');
    }
}

function renderMenu(items) {
    const grid = document.getElementById('menu-grid');
    if (!grid) return;
    
    const categoryIcons = {
        'Glavna jela': '🍖',
        'Juhe': '🍲',
        'Salate': '🥗',
        'Deserti': '🍰',
        'Piće': '🥤'
    };
    
    grid.innerHTML = items.map(item => `
        <div class="menu-card ${!item.is_available ? 'menu-card-unavailable' : ''}">
            <div class="menu-card-image">
                ${categoryIcons[item.category] || '🍽️'}
            </div>
            <div class="menu-card-content">
                <span class="menu-card-category">${item.category || 'Ostalo'}</span>
                <h3 class="menu-card-name">${item.name}</h3>
                <p class="menu-card-description">${item.description || ''}</p>
                <div class="menu-card-footer">
                    <span class="menu-card-price">${parseFloat(item.price).toFixed(2)} €</span>
                    ${item.is_available 
                        ? `<button class="btn btn-primary" onclick="addToCart(${item.id})">+ Dodaj</button>`
                        : '<span class="unavailable-badge">Nedostupno</span>'
                    }
                </div>
            </div>
        </div>
    `).join('');
}

function renderCategoryFilters() {
    const container = document.getElementById('category-filters');
    if (!container) return;
    
    const categories = [...new Set(menuItems.map(item => item.category).filter(Boolean))];
    
    container.innerHTML = `
        <button class="filter-btn active" data-category="all">Sve</button>
        ${categories.map(cat => `
            <button class="filter-btn" data-category="${cat}">${cat}</button>
        `).join('')}
    `;
    
    container.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const category = btn.dataset.category;
            const filtered = category === 'all' 
                ? menuItems 
                : menuItems.filter(item => item.category === category);
            renderMenu(filtered);
        });
    });
}

// ============ CART ============

function addToCart(itemId) {
    const item = menuItems.find(i => i.id === itemId);
    if (!item || !item.is_available) return;
    
    const existingItem = cart.find(i => i.id === itemId);
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            id: item.id,
            name: item.name,
            price: parseFloat(item.price),
            quantity: 1
        });
    }
    
    saveCart();
    updateCartUI();
    showToast(`${item.name} dodan u košaricu`, 'success');
}

function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    saveCart();
    updateCartUI();
}

function updateQuantity(itemId, delta) {
    const item = cart.find(i => i.id === itemId);
    if (!item) return;
    
    item.quantity += delta;
    if (item.quantity <= 0) {
        removeFromCart(itemId);
    } else {
        saveCart();
        updateCartUI();
    }
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function updateCartUI() {
    // Update cart count (both desktop and mobile)
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.querySelectorAll('.cart-count').forEach(el => {
        el.textContent = totalItems;
    });
    
    // Update cart items
    const cartItemsEl = document.getElementById('cart-items');
    const cartSummaryEl = document.getElementById('cart-summary');
    
    if (!cartItemsEl) return;
    
    if (cart.length === 0) {
        cartItemsEl.innerHTML = '<p class="empty-cart">Košarica je prazna</p>';
        if (cartSummaryEl) cartSummaryEl.style.display = 'none';
        return;
    }
    
    cartItemsEl.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${item.price.toFixed(2)} € / kom</div>
            </div>
            <div class="cart-item-quantity">
                <button class="quantity-btn" onclick="updateQuantity(${item.id}, -1)">−</button>
                <span class="quantity-value">${item.quantity}</span>
                <button class="quantity-btn" onclick="updateQuantity(${item.id}, 1)">+</button>
            </div>
            <div class="cart-item-total">${(item.price * item.quantity).toFixed(2)} €</div>
            <span class="cart-item-remove" onclick="removeFromCart(${item.id})">🗑️</span>
        </div>
    `).join('');
    
    // Update total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const totalEl = document.getElementById('total-price');
    if (totalEl) totalEl.textContent = `${total.toFixed(2)} €`;
    
    if (cartSummaryEl) cartSummaryEl.style.display = 'block';
}

function setDefaultPickupTime() {
    const input = document.getElementById('pickup-time');
    if (!input) return;
    
    const now = new Date();
    now.setHours(now.getHours() + 2);
    now.setMinutes(0);
    
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    
    input.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    input.min = input.value;
}

async function submitOrder() {
    if (!currentUser) {
        showToast('Molimo prijavite se za naručivanje', 'warning');
        showLogin();
        return;
    }
    
    if (cart.length === 0) {
        showToast('Košarica je prazna', 'warning');
        return;
    }
    
    const pickupTime = document.getElementById('pickup-time').value;
    const note = document.getElementById('order-note').value;
    
    if (!pickupTime) {
        showToast('Odaberite vrijeme preuzimanja', 'warning');
        return;
    }
    
    const orderData = {
        pickup_time: new Date(pickupTime).toISOString(),
        note: note || null,
        items: cart.map(item => ({
            menu_item_id: item.id,
            quantity: item.quantity
        }))
    };
    
    try {
        const response = await fetch(`${API_URL}/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(orderData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Greška pri naručivanju');
        }
        
        // Clear cart
        cart = [];
        saveCart();
        updateCartUI();
        
        showToast('Narudžba uspješno poslana! 🎉', 'success');
        
        // Go to orders
        document.querySelector('[data-section="orders"]').click();
        
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// ============ ORDERS ============

async function loadMyOrders() {
    const container = document.getElementById('orders-list');
    if (!container) return;
    
    if (!currentUser) {
        container.innerHTML = '<p class="login-prompt">Prijavi se za pregled narudžbi</p>';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/orders/my`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const orders = await response.json();
        renderOrders(orders, container);
        
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="empty-cart">Greška pri učitavanju narudžbi</p>';
    }
}

function renderOrders(orders, container, isAdmin = false) {
    if (orders.length === 0) {
        container.innerHTML = '<p class="empty-cart">Nema narudžbi</p>';
        return;
    }
    
    const statusLabels = {
        pending: 'Na čekanju',
        confirmed: 'Potvrđena',
        ready: 'Spremna',
        completed: 'Završena',
        cancelled: 'Otkazana'
    };
    
    container.innerHTML = orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <div>
                    <div class="order-id">Narudžba #${order.id}</div>
                    <div class="order-date">${formatDate(order.created_at)}</div>
                </div>
                <span class="order-status status-${order.status}">${statusLabels[order.status]}</span>
            </div>
            <div class="order-items">
                ${order.items.map(item => `
                    <div class="order-item-row">
                        <span>${item.quantity}x ${item.menu_item_name || 'Artikl #' + item.menu_item_id}</span>
                        <span>${(parseFloat(item.unit_price) * item.quantity).toFixed(2)} €</span>
                    </div>
                `).join('')}
            </div>
            <div class="order-footer">
                <div>
                    <div class="order-total">${parseFloat(order.total_price).toFixed(2)} €</div>
                    <div class="order-pickup">Preuzimanje: ${formatDate(order.pickup_time)}</div>
                    ${order.note ? `<div class="order-note-text">📝 ${order.note}</div>` : ''}
                </div>
                ${isAdmin ? `
                    <div class="order-actions">
                        ${order.status === 'pending' ? `
                            <button class="btn btn-small btn-success" onclick="updateOrderStatus(${order.id}, 'confirmed')">Potvrdi</button>
                            <button class="btn btn-small btn-danger" onclick="updateOrderStatus(${order.id}, 'cancelled')">Otkaži</button>
                        ` : ''}
                        ${order.status === 'confirmed' ? `
                            <button class="btn btn-small btn-warning" onclick="updateOrderStatus(${order.id}, 'ready')">Spremno</button>
                        ` : ''}
                        ${order.status === 'ready' ? `
                            <button class="btn btn-small btn-primary" onclick="updateOrderStatus(${order.id}, 'completed')">Završi</button>
                        ` : ''}
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// ============ ADMIN ============

function initAdminPage() {
    loadAdminOrders();
    loadAdminMenu();
    
    // Setup hamburger menu
    setupHamburgerMenu();
    
    // Setup navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            showSection(section);
            
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Close mobile menu
            const hamburger = document.getElementById('hamburger');
            const mobileMenu = document.getElementById('mobileMenu');
            if (hamburger && mobileMenu) {
                hamburger.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Setup order filters
    document.querySelectorAll('.order-filters .filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.order-filters .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadAdminOrders(btn.dataset.status);
        });
    });
}

async function loadAdminOrders(status = 'all') {
    const container = document.getElementById('admin-orders-list');
    if (!container) return;
    
    try {
        let url = `${API_URL}/orders/`;
        if (status !== 'all') {
            url += `?status=${status}`;
        }
        
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const orders = await response.json();
        renderOrders(orders, container, true);
        
    } catch (error) {
        console.error('Error loading orders:', error);
        container.innerHTML = '<p class="empty-cart">Greška pri učitavanju narudžbi</p>';
    }
}

async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`${API_URL}/orders/${orderId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ status })
        });
        
        if (!response.ok) throw new Error('Greška pri ažuriranju');
        
        showToast('Status ažuriran', 'success');
        loadAdminOrders();
        
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function loadAdminMenu() {
    const container = document.getElementById('admin-menu-list');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_URL}/menu/?available_only=false`);
        const items = await response.json();
        
        container.innerHTML = items.map(item => `
            <div class="admin-menu-card">
                <div class="admin-menu-info">
                    <h3>${item.name}</h3>
                    <p>${item.description || 'Bez opisa'}</p>
                    <div class="admin-menu-meta">
                        <span class="admin-menu-price">${parseFloat(item.price).toFixed(2)} €</span>
                        <span>${item.category || 'Bez kategorije'}</span>
                        <span class="order-status ${item.is_available ? 'status-ready' : 'status-cancelled'}">
                            ${item.is_available ? 'Dostupno' : 'Nedostupno'}
                        </span>
                    </div>
                </div>
                <div class="admin-menu-actions">
                    <button class="btn btn-small btn-outline" onclick="editItem(${item.id})">Uredi</button>
                    <button class="btn btn-small btn-danger" onclick="deleteItem(${item.id})">Obriši</button>
                </div>
            </div>
        `).join('');
        
        // Store for editing
        menuItems = items;
        
    } catch (error) {
        console.error('Error loading menu:', error);
    }
}

function showAddItemModal() {
    document.getElementById('item-modal-title').textContent = 'Dodaj Artikl';
    document.getElementById('item-form').reset();
    document.getElementById('item-id').value = '';
    document.getElementById('item-available').checked = true;
    document.getElementById('item-modal').classList.add('active');
}

function editItem(itemId) {
    const item = menuItems.find(i => i.id === itemId);
    if (!item) return;
    
    document.getElementById('item-modal-title').textContent = 'Uredi Artikl';
    document.getElementById('item-id').value = item.id;
    document.getElementById('item-name').value = item.name;
    document.getElementById('item-description').value = item.description || '';
    document.getElementById('item-price').value = item.price;
    document.getElementById('item-category').value = item.category || 'Glavna jela';
    document.getElementById('item-available').checked = item.is_available;
    document.getElementById('item-modal').classList.add('active');
}

async function handleItemSubmit(e) {
    e.preventDefault();
    
    const itemId = document.getElementById('item-id').value;
    const data = {
        name: document.getElementById('item-name').value,
        description: document.getElementById('item-description').value || null,
        price: document.getElementById('item-price').value,
        category: document.getElementById('item-category').value,
        is_available: document.getElementById('item-available').checked
    };
    
    try {
        const url = itemId ? `${API_URL}/menu/${itemId}` : `${API_URL}/menu/`;
        const method = itemId ? 'PATCH' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Greška pri spremanju');
        }
        
        closeModal('item-modal');
        showToast(itemId ? 'Artikl ažuriran' : 'Artikl dodan', 'success');
        loadAdminMenu();
        
    } catch (error) {
        document.getElementById('item-error').textContent = error.message;
    }
}

async function deleteItem(itemId) {
    if (!confirm('Jeste li sigurni da želite obrisati ovaj artikl?')) return;
    
    try {
        const response = await fetch(`${API_URL}/menu/${itemId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Greška pri brisanju');
        
        showToast('Artikl obrisan', 'success');
        loadAdminMenu();
        
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// ============ UTILITIES ============

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('hr-HR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icons[type]}</span>
        <span class="toast-message">${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Close modals on outside click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});
