/**
 * Telegram Mini App - Clicker Game Frontend
 * Main application script for the web app
 */

// Telegram Web App API
const tg = window.Telegram.WebApp;

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Application state
let currentUser = null;
let gameState = {
    clicks: 0,
    balance: 0,
    lastBalance: 0
};

/**
 * Initialize Telegram Web App
 */
function initializeTelegram() {
    tg.ready();
    tg.expand();
    
    // Get user data from Telegram
    const user = tg.initDataUnsafe?.user;
    
    if (user) {
        currentUser = {
            user_id: user.id,
            first_name: user.first_name,
            username: user.username,
            is_premium: user.is_premium
        };
        
        console.log('[INFO] Telegram user authorized:', currentUser.first_name);
    } else {
        // Fallback for local testing
        currentUser = {
            user_id: Math.floor(Math.random() * 1000000),
            first_name: 'Guest',
            username: 'guest'
        };
        console.warn('[WARN] Running in test mode without Telegram authentication');
    }
    
    initializeApp();
}

/**
 * Initialize the application
 */
async function initializeApp() {
    console.log('[INFO] Initializing app for user:', currentUser.first_name);
    
    // Load user data from backend
    await loadUserData();
    
    // Setup event listeners
    setupEventListeners();
    
    // Load leaderboard
    await loadLeaderboard();
    
    // Update UI
    updateUserDisplay();
}

/**
 * Load user data from backend
 */
async function loadUserData() {
    try {
        const response = await fetch(`${API_BASE_URL}/user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUser.user_id,
                first_name: currentUser.first_name,
                username: currentUser.username
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            gameState.clicks = data.clicks || 0;
            gameState.balance = data.balance || 0;
            gameState.lastBalance = data.balance || 0;
            console.log('[OK] User data loaded:', data);
        } else {
            console.error('[ERROR] Failed to load user data:', data);
        }
    } catch (error) {
        console.error('[ERROR] Network error loading user data:', error);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    const clickButton = document.getElementById('clickButton');
    const withdrawButton = document.getElementById('withdrawButton');
    const statsButton = document.getElementById('statsButton');
    const leaderboardButton = document.getElementById('leaderboardButton');
    const refreshButton = document.getElementById('refreshButton');
    
    // Click button
    if (clickButton) {
        clickButton.addEventListener('click', handleClick);
    }
    
    // Withdraw button
    if (withdrawButton) {
        withdrawButton.addEventListener('click', handleWithdraw);
    }
    
    // Stats button
    if (statsButton) {
        statsButton.addEventListener('click', showStats);
    }
    
    // Leaderboard button
    if (leaderboardButton) {
        leaderboardButton.addEventListener('click', showLeaderboard);
    }
    
    // Refresh button
    if (refreshButton) {
        refreshButton.addEventListener('click', async () => {
            await loadUserData();
            updateUserDisplay();
        });
    }
}

/**
 * Handle click button - Award coins
 */
async function handleClick() {
    try {
        const response = await fetch(`${API_BASE_URL}/click`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUser.user_id })
        });
        
        const data = await response.json();
        if (response.ok) {
            gameState.clicks = data.clicks;
            gameState.balance = data.balance;
            
            // Animate the balance increase
            animateBalanceIncrease();
            updateUserDisplay();
            
            console.log('[OK] Click registered. Balance:', gameState.balance);
        } else {
            console.error('[ERROR] Click failed:', data);
        }
    } catch (error) {
        console.error('[ERROR] Network error during click:', error);
    }
}

/**
 * Handle withdrawal request
 */
async function handleWithdraw() {
    const amount = parseInt(prompt('Enter amount to withdraw (min 100):', '100'));
    
    if (isNaN(amount) || amount < 100) {
        alert('Invalid amount. Minimum is 100 coins.');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/withdraw`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUser.user_id,
                amount: amount
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            gameState.balance = data.balance;
            updateUserDisplay();
            alert(`Withdrawal successful! New balance: ${data.balance}`);
            console.log('[OK] Withdrawal completed:', data);
        } else {
            alert(`Withdrawal failed: ${data.error}`);
            console.error('[ERROR] Withdrawal failed:', data);
        }
    } catch (error) {
        console.error('[ERROR] Network error during withdrawal:', error);
        alert('Network error. Please try again.');
    }
}

/**
 * Show user statistics
 */
async function showStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUser.user_id })
        });
        
        const data = await response.json();
        if (response.ok) {
            const statsText = `
📊 Your Statistics
━━━━━━━━━━━━━━━━━━━━
👤 Name: ${data.first_name}
🆔 ID: ${data.user_id}
👉 Clicks: ${data.total_clicks}
💰 Balance: ${data.current_balance}
📅 Member since: ${new Date(data.created_at).toLocaleDateString()}
            `;
            alert(statsText);
            console.log('[OK] Stats loaded:', data);
        } else {
            alert('Failed to load statistics');
            console.error('[ERROR] Stats failed:', data);
        }
    } catch (error) {
        console.error('[ERROR] Network error loading stats:', error);
        alert('Network error. Please try again.');
    }
}

/**
 * Show leaderboard
 */
async function loadLeaderboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/leaderboard`);
        const data = await response.json();
        
        if (response.ok && data.leaderboard) {
            displayLeaderboard(data.leaderboard);
            console.log('[OK] Leaderboard loaded');
        } else {
            console.error('[ERROR] Leaderboard load failed:', data);
        }
    } catch (error) {
        console.error('[ERROR] Network error loading leaderboard:', error);
    }
}

/**
 * Show leaderboard in alert
 */
async function showLeaderboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/leaderboard`);
        const data = await response.json();
        
        if (response.ok && data.leaderboard) {
            let leaderboardText = '🏆 Top 10 Players\n━━━━━━━━━━━━━━━━━━━━\n';
            data.leaderboard.forEach((player, index) => {
                leaderboardText += `${index + 1}. ${player.first_name} - ${player.balance} coins\n`;
            });
            
            alert(leaderboardText);
            console.log('[OK] Leaderboard displayed');
        } else {
            alert('Failed to load leaderboard');
        }
    } catch (error) {
        console.error('[ERROR] Failed to show leaderboard:', error);
        alert('Network error. Please try again.');
    }
}

/**
 * Display leaderboard in the page
 */
function displayLeaderboard(players) {
    const leaderboardDiv = document.getElementById('leaderboard');
    if (!leaderboardDiv) return;
    
    let html = '<h2>🏆 Top Players</h2><div class="leaderboard-list">';
    players.forEach((player, index) => {
        const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '📍';
        html += `
            <div class="leaderboard-item">
                <span>${medal} ${index + 1}</span>
                <span>${player.first_name}</span>
                <span>${player.balance} 💰</span>
            </div>
        `;
    });
    html += '</div>';
    
    leaderboardDiv.innerHTML = html;
}

/**
 * Animate balance increase
 */
function animateBalanceIncrease() {
    const balanceDisplay = document.getElementById('balance');
    if (balanceDisplay) {
        balanceDisplay.classList.add('balance-increase');
        setTimeout(() => {
            balanceDisplay.classList.remove('balance-increase');
        }, 300);
    }
}

/**
 * Update user interface display
 */
function updateUserDisplay() {
    const userNameEl = document.getElementById('userName');
    const clicksEl = document.getElementById('clicks');
    const balanceEl = document.getElementById('balance');
    
    if (userNameEl) {
        userNameEl.textContent = `${currentUser.first_name}${currentUser.is_premium ? ' ⭐' : ''}`;
    }
    
    if (clicksEl) {
        clicksEl.textContent = gameState.clicks;
    }
    
    if (balanceEl) {
        balanceEl.textContent = gameState.balance;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeTelegram);

// Log when page loads
console.log('[INFO] Telegram Mini App loaded');
