document.addEventListener('DOMContentLoaded', () => {
    // --- TradingView Integration ---
    let tvWidget = null;

    function initTradingView(symbol) {
        // Clear old widget
        const container = document.getElementById('tradingview-widget-container');
        container.innerHTML = '';

        tvWidget = new TradingView.widget({
            "autosize": true,
            "symbol": `BINANCE:${symbol}.P`, // .P suffix for Perpetual Futures on Binance
            "interval": "15",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "backgroundColor": "#161a1e",
            "gridColor": "#2b3139",
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": "tradingview-widget-container",
            "toolbar_bg": "#161a1e",
            "studies": [
                "Volume@tv-basicstudies"
            ],
            "disabled_features": [
                "header_symbol_search",
                "header_compare"
            ]
        });

        // Update header
        document.getElementById('header-symbol').textContent = symbol;
    }

    // --- DOM Elements ---
    const els = {
        symbolInput: document.getElementById('symbol'),
        balance: document.getElementById('usdt-balance'),
        form: document.getElementById('trade-form'),
        tabs: document.querySelectorAll('.tab'),
        orderType: document.getElementById('order-type'),
        priceGroup: document.getElementById('price-group'),
        priceInput: document.getElementById('price'),
        qtyInput: document.getElementById('quantity'),
        sideBuy: document.getElementById('side-buy'),
        sideSell: document.getElementById('side-sell'),
        submitBtn: document.getElementById('submit-btn'),
        ordersBody: document.getElementById('orders-body'),
        refreshBtn: document.getElementById('refresh-orders'),
        toast: document.getElementById('toast'),
    };

    // --- State & Sync Logic ---
    let currentSymbol = els.symbolInput.value.toUpperCase();
    initTradingView(currentSymbol);

    // When user changes symbol and clicks out or hits enter, update chart
    els.symbolInput.addEventListener('change', (e) => {
        const newSymbol = e.target.value.toUpperCase().trim();
        if (newSymbol && newSymbol !== currentSymbol) {
            currentSymbol = newSymbol;
            initTradingView(currentSymbol);
            updateSubmitButtonText();
        }
    });

    // --- Tab Logic (Market vs Limit) ---
    els.tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            // Remove active from all
            els.tabs.forEach(t => t.classList.remove('active'));
            // Add to clicked
            e.target.classList.add('active');

            const typeText = e.target.dataset.tab.toUpperCase(); // MARKET or LIMIT
            els.orderType.value = typeText;

            if (typeText === 'LIMIT') {
                els.priceGroup.style.display = 'flex';
                els.priceInput.setAttribute('required', 'true');
            } else {
                els.priceGroup.style.display = 'none';
                els.priceInput.removeAttribute('required');
            }
        });
    });

    // --- Side Logic (Buy vs Sell Button Updates) ---
    function updateSubmitButtonText() {
        const isBuy = els.sideBuy.checked;
        els.submitBtn.textContent = `${isBuy ? 'Buy' : 'Sell'} ${currentSymbol}`;
        els.submitBtn.className = `btn ${isBuy ? 'buy-btn' : 'sell-btn'}`;
    }
    els.sideBuy.addEventListener('change', updateSubmitButtonText);
    els.sideSell.addEventListener('change', updateSubmitButtonText);

    // --- Utilities ---
    const formatNum = (num, decimals = 2) => Number(num).toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });

    function showToast(message, type = 'success') {
        els.toast.textContent = message;
        els.toast.className = `toast show ${type}`;
        setTimeout(() => { els.toast.className = 'toast'; }, 3000);
    }

    // --- API Interactions ---
    async function fetchBalance() {
        try {
            const res = await fetch('/api/balance');
            const data = await res.json();
            if (data.balance !== undefined) els.balance.textContent = formatNum(data.balance);
        } catch (e) {
            console.error(e);
        }
    }

    async function fetchOrders() {
        try {
            const res = await fetch('/api/orders');
            const data = await res.json();
            renderOrders(data.orders || []);
        } catch (e) {
            console.error(e);
        }
    }

    function renderOrders(orders) {
        if (!orders.length) {
            els.ordersBody.innerHTML = `<tr><td colspan="7" class="empty-state">No open orders</td></tr>`;
            return;
        }

        els.ordersBody.innerHTML = orders.map(o => {
            const date = new Date(o.updateTime || o.time).toLocaleTimeString();
            return `
            <tr>
                <td class="num">${date}</td>
                <td><strong>${o.symbol}</strong></td>
                <td>${o.type}</td>
                <td class="${o.side === 'BUY' ? 'text-buy' : 'text-sell'}">${o.side}</td>
                <td class="num right">${formatNum(o.price, 2)}</td>
                <td class="num right">${formatNum(o.origQty, 4)}</td>
                <td class="right">
                    <button class="cancel-btn" data-symbol="${o.symbol}" data-id="${o.orderId}">Cancel</button>
                </td>
            </tr>
            `;
        }).join('');

        document.querySelectorAll('.cancel-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const b = e.target;
                b.textContent = '...';
                try {
                    await fetch(`/api/orders/${b.dataset.symbol}/${b.dataset.id}`, { method: 'DELETE' });
                    showToast('Order canceled', 'success');
                    fetchOrders();
                    fetchBalance();
                } catch (err) {
                    showToast('Cancel failed', 'error');
                }
            });
        });
    }

    // --- Form Submit ---
    els.form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            symbol: els.symbolInput.value.trim().toUpperCase(),
            side: els.sideBuy.checked ? 'BUY' : 'SELL',
            order_type: els.orderType.value,
            quantity: parseFloat(els.qtyInput.value),
            price: els.orderType.value === 'LIMIT' ? parseFloat(els.priceInput.value) : null
        };

        const origBtnText = els.submitBtn.textContent;
        els.submitBtn.textContent = 'Sending...';
        els.submitBtn.disabled = true;

        try {
            const res = await fetch('/api/trade', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || 'Trade failed');

            showToast('Order successful', 'success');
            setTimeout(fetchOrders, 500);
            setTimeout(fetchBalance, 500);

        } catch (err) {
            showToast(err.message, 'error');
        } finally {
            els.submitBtn.textContent = origBtnText;
            els.submitBtn.disabled = false;
        }
    });

    els.refreshBtn.addEventListener('click', () => { fetchOrders(); fetchBalance(); });

    // --- Boot ---
    updateSubmitButtonText();
    fetchBalance();
    fetchOrders();
    setInterval(() => { fetchBalance(); fetchOrders(); }, 5000); // 5 sec poll
});
