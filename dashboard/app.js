let audioCtx;
let currentOsc;
let currentGain;
let isPlaying = false;
let activeTrackId = null;
let activeTrack = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

async function togglePlay(track) {
    initAudio();
    activeTrack = track;

    if (activeTrackId === track.id) {
        if (isPlaying) {
            await audioCtx.suspend();
            isPlaying = false;
            updateUIState();
        } else {
            await audioCtx.resume();
            isPlaying = true;
            updateUIState();
        }
        return;
    }

    // New track selected
    stopAudio();
    activeTrackId = track.id;
    startGenerativeAudio(track);
}

function startGenerativeAudio(track) {
    currentOsc = audioCtx.createOscillator();
    currentGain = audioCtx.createGain();

    currentOsc.type = (track.synth || 'sine').toLowerCase();
    const keyFreqs = { "C": 261.63, "D": 293.66, "E": 329.63, "F": 349.23, "G": 392.00, "A": 440.00, "B": 493.88 };
    let baseFreq = keyFreqs[track.key.charAt(0)] || 440;

    currentOsc.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);

    const pulseRate = 60 / track.tempo;
    currentGain.gain.setValueAtTime(0, audioCtx.currentTime);

    // Create a loop of pulses
    for (let i = 0; i < 60; i++) {
        currentGain.gain.exponentialRampToValueAtTime(0.2, audioCtx.currentTime + (i * pulseRate));
        currentGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + (i * pulseRate) + 0.2);
    }

    currentOsc.connect(currentGain);
    currentGain.connect(audioCtx.destination);

    currentOsc.start();
    isPlaying = true;
    updateUIState();
}

function stopAudio() {
    if (currentOsc) {
        try { currentOsc.stop(); } catch (e) { }
        currentOsc = null;
    }
    activeTrackId = null;
    isPlaying = false;
    updateUIState();
}

function updateUIState() {
    const cards = document.querySelectorAll('.track-card');
    cards.forEach(card => {
        const trackId = card.getAttribute('data-id');
        const playBtn = card.querySelector('.play-button');

        if (trackId === activeTrackId) {
            card.classList.add('playing');
            playBtn.textContent = isPlaying ? '⏸' : '▶';
        } else {
            card.classList.remove('playing');
            playBtn.textContent = '▶';
        }
    });

    // Update Footer
    const footer = document.getElementById('player-footer');
    const footerPlayPause = document.getElementById('footer-play-pause');
    if (activeTrackId) {
        footer.classList.add('active');
        document.getElementById('footer-title').textContent = activeTrack.title;
        document.getElementById('footer-sub').textContent = `${activeTrack.genre} • ${activeTrack.tempo} BPM`;
        footerPlayPause.textContent = isPlaying ? '⏸' : '▶';
    } else {
        footer.classList.remove('active');
    }
}

function togglePlayFromFooter() {
    if (activeTrack) togglePlay(activeTrack);
}

function toggleSidebar(side) {
    const sidebar = document.getElementById(`${side}-sidebar`);
    sidebar.classList.toggle('collapsed');
    const toggleBtn = document.getElementById(`${side}-toggle`);

    if (side === 'left') {
        toggleBtn.textContent = sidebar.classList.contains('collapsed') ? 'R' : 'L';
    } else {
        toggleBtn.textContent = sidebar.classList.contains('collapsed') ? 'L' : 'R';
    }
}

function switchView(viewName, element) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    document.getElementById(`${viewName}-view`).classList.add('active');
    if (element) {
        element.classList.add('active');
    } else {
        // Fallback for direct calls
        document.querySelector(`.nav-link[onclick*="${viewName}"]`)?.classList.add('active');
    }
}

let currentFilter = 'all';
let searchQuery = '';

function setCatalogFilter(filter) {
    currentFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.toLowerCase() === filter.toLowerCase() || (filter === 'all' && btn.textContent === 'All'));
    });
    filterCatalog();
}

function filterCatalog() {
    searchQuery = document.getElementById('catalog-search')?.value.toLowerCase() || '';
    const fullGrid = document.getElementById('full-catalog-grid');
    if (!fullGrid) return;

    fullGrid.innerHTML = '';
    const filtered = globalState.catalog.filter(track => {
        const matchesSearch = track.title.toLowerCase().includes(searchQuery) || track.genre.toLowerCase().includes(searchQuery);
        const matchesFilter = currentFilter === 'all' || track.genre.toLowerCase().includes(currentFilter.toLowerCase());
        return matchesSearch && matchesFilter;
    });

    filtered.forEach(track => {
        const card = createTrackCard(track);
        fullGrid.appendChild(card);
    });
}

function createTrackCard(track) {
    const card = document.createElement('div');
    card.className = 'track-card';
    card.setAttribute('data-id', track.id);
    if (activeTrackId === track.id) card.classList.add('playing');

    // Generate static visualizer
    let waveHTML = '<div class="static-wave">';
    for (let i = 0; i < 16; i++) {
        const height = 20 + Math.random() * 60; // 20% to 80% height
        waveHTML += `<div class="s-bar" style="height: ${height}%;"></div>`;
    }
    waveHTML += '</div>';

    card.innerHTML = `
        <div class="track-visual">
            ${waveHTML}
            <div class="controls-overlay"><div class="play-button">${(activeTrackId === track.id && isPlaying) ? '⏸' : '▶'}</div><div class="stop-button" onclick="event.stopPropagation(); stopAudio();">⏹</div></div>
        </div>
        <div class="track-meta"><h3>${track.title}</h3><p>${track.genre} • ${track.tempo} BPM</p>
        <div class="tag-row"><span class="tag accent">${track.vocal_config?.emotion || 'Upbeat'}</span><span class="tag">${track.key} ${track.scale}</span></div></div>`;
    card.onclick = () => togglePlay(track);
    return card;
}

function simulateMarketingAction(type) {
    const actions = {
        boost: "🚀 Viral Boost initiated on TikTok & Instagram! Targeted reach: +50k potential listeners."
    };
    alert(actions[type]);
}

let isSimulating = false;
let localBalance = 0;
let localSubs = 0;

function simulateBillingAction(type) {
    if (type === 'withdraw') {
        if (localBalance <= 0) return alert("Insufficient funds to withdraw.");

        const amount = localBalance;
        const btn = document.querySelector('.btn-withdraw'); // Assuming I'll add this class or use existing
        const originalText = btn ? btn.textContent : 'Withdraw';
        if (btn) btn.textContent = 'Processing...';

        setTimeout(() => {
            // Update Balance
            localBalance = 0;
            document.getElementById('wallet-balance').innerHTML = '$0.00';

            // Add Log
            const history = document.getElementById('billing-history');
            const item = document.createElement('div');
            item.className = 'transaction-item';
            item.innerHTML = `<div><div style="font-weight:600">Transfer to Bank</div><div style="font-size:0.7rem;opacity:0.6">Just now</div></div><div class="amount minus">-$${amount.toFixed(2)}</div>`;
            history.insertBefore(item, history.firstChild);

            if (btn) btn.textContent = originalText;
            alert(`Successfully withdrew $${amount.toFixed(2)} to your bank account.`);
        }, 1500);
        return;
    }

    if (type === 'simulation') {
        if (isSimulating) return;
        isSimulating = true;
        const btn = document.querySelector('button[onclick*="simulation"]');
        if (btn) btn.disabled = true;

        let day = 1;
        const interval = setInterval(() => {
            // Growth Logic
            const newUsers = Math.floor(Math.random() * 5) + 1;
            const revenue = newUsers * 10; // High value for demo

            localSubs += newUsers;
            localBalance += revenue;

            // UI Updates
            document.getElementById('wallet-balance').textContent = `$${localBalance.toFixed(2)}`;
            document.getElementById('wallet-balance').style.color = '#00ff66';
            setTimeout(() => document.getElementById('wallet-balance').style.color = '', 300);

            document.getElementById('active-subs').textContent = localSubs;

            // Feed Update
            const feed = document.querySelector('.news-feed');
            const feedItem = document.createElement('div');
            feedItem.className = 'feed-item billing';
            feedItem.innerHTML = `<span class="feed-date">Live Simulation Day ${day}</span><div>🚀 Growth Spike! +${newUsers} new subscribers joined.</div>`;
            feed.insertBefore(feedItem, feed.firstChild);

            day++;
            if (day > 10) {
                clearInterval(interval);
                isSimulating = false;
                if (btn) btn.disabled = false;
                alert("Growth simulation complete!");
            }
        }, 800);
        return;
    }

    if (type === 'audit') {
        alert("Internal financial audit complete. 100% compliance with Nimbus standards.");
    }

    if (type === 'boost') {
        const btn = document.querySelector('button[onclick*="boost"]');
        if (btn) btn.textContent = 'Boosting...';
        setTimeout(() => {
            alert("🚀 Viral Boost initiated! Checking social metrics...");
            if (btn) btn.textContent = 'Launch Viral Boost';
        }, 1000);
    }
}

let globalState = null;

function renderDashboard(state) {
    globalState = state;

    // Initialize local state if not simulating to keep in sync, otherwise respect local simulation
    if (!isSimulating && state) {
        // Only override if we haven't drastically changed it locally (basic sync)
        // For this demo, we'll assume backend is truth UNLESS we are in "demo mode" which we just triggered
        // But since we can't write back, we'll settle for:
        // If we haven't touched localBalance yet (it's 0), sync it.
        // If we HAVE touched it, we might want to keep our local version for the demo content.

        // Simple approach: Only sync if we aren't currently running the active interval
        // But to prevent the "reset" after 10 days, we'll just check if local is vastly different

        if (localBalance === 0) localBalance = state.balance;
        if (localSubs === 0) localSubs = state.catalog ? (state.catalog.length * 4) + 12 : 0;
    }

    // Stats Update
    document.getElementById('balance').innerHTML = `<span class="stat-label">Total Revenue</span><div class="stat-value">$${localBalance.toFixed(2)}</div>`;
    document.getElementById('track-count').innerHTML = `<span class="stat-label">Catalog Size</span><div class="stat-value">${state.catalog.length}</div>`;
    const playlistCount = Object.keys(state.playlists || {}).length;
    document.getElementById('playlist-stat').innerHTML = `<span class="stat-label">AI Playlists</span><div class="stat-value">${playlistCount}</div>`;

    // Dashboard Recent
    const catalogGrid = document.querySelector('.catalog-grid:not(#full-catalog-grid)');
    if (catalogGrid && catalogGrid.children.length === 0) { // Only render if empty to save re-renders
        [...state.catalog].reverse().slice(0, 4).forEach(track => {
            catalogGrid.appendChild(createTrackCard(track));
        });
    }

    // Full Catalog View - Only if view is active
    if (document.getElementById('catalog-view').classList.contains('active')) {
        // We won't re-render full grid every 5s to avoid losing search state
        if (document.getElementById('full-catalog-grid').children.length === 0) filterCatalog();
    }

    // Marketing View
    const campaignList = document.getElementById('campaign-list');
    if (campaignList && campaignList.children.length === 0) {
        const recentMarketing = (state.marketing_log || []).slice().reverse().slice(0, 4);
        recentMarketing.forEach(log => {
            const item = document.createElement('div');
            item.className = 'campaign-item';
            item.innerHTML = `<h4>${log.platform || 'Social Media'} Promotion</h4><p>${log.message || log.copy}</p>`;
            campaignList.appendChild(item);
        });
    }

    // Billing View
    const walletEl = document.getElementById('wallet-balance');
    // Only update from state if we aren't in the middle of a simulation visual
    if (!isSimulating && walletEl.textContent === '$0.00') {
        walletEl.textContent = `$${localBalance.toFixed(2)}`;
        document.getElementById('active-subs').textContent = localSubs;
    }

    const billingHistory = document.getElementById('billing-history');
    if (billingHistory.children.length === 0) {
        (state.billing_log || []).slice().reverse().slice(0, 5).forEach(log => {
            const item = document.createElement('div');
            item.className = 'transaction-item';
            item.innerHTML = `<div><div style="font-weight:600">Nimbus Subscription Pool</div><div style="font-size:0.7rem;opacity:0.6">${new Date(log.timestamp).toLocaleDateString()}</div></div><div class="amount plus">+$1.00</div>`;
            billingHistory.appendChild(item);
        });
    }

    // Feed
    const feed = document.querySelector('.news-feed');
    if (feed.children.length === 0) {
        const allLogs = [
            ...(state.music_log || []).map(l => ({ ...l, type: 'music' })),
            ...(state.billing_log || []).map(l => ({ ...l, type: 'billing' })),
            ...(state.marketing_log || []).map(l => ({ ...l, type: 'marketing' }))
        ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        allLogs.slice(0, 15).forEach(log => {
            const item = document.createElement('div');
            item.className = `feed-item ${log.type}`;
            item.innerHTML = `<span class="feed-date">${new Date(log.timestamp).toLocaleDateString()}</span><div>${log.message || log.copy}</div>`;
            feed.appendChild(item);
        });
    }

    updateUIState();
}

async function loadState() {
    // If we are simulating, don't fetch/overwrite state or the UI will jump
    if (isSimulating) return;

    try {
        const response = await fetch('../data/company_state.json?t=' + Date.now());
        const state = await response.json();
        renderDashboard(state);
    } catch (e) { console.error("Sync error"); }
}

loadState();
setInterval(loadState, 5000);
