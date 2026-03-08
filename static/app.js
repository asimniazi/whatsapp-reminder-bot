/* ═══════════════════════════════════════
   REMINDER BOT — app.js
═══════════════════════════════════════ */

let notifyType = 'message';

/* ── Theme ── */
function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  localStorage.setItem('rb-theme', isDark ? 'light' : 'dark');
}

function loadTheme() {
  const saved = localStorage.getItem('rb-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
}

/* ── Sidebar (mobile) ── */
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('open');
}

/* ── View Navigation ── */
function showView(id, el) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.getElementById('view-' + id).classList.add('active');
  if (el) el.classList.add('active');

  const titles = { dashboard: 'Dashboard', reminders: 'Reminders', guide: 'How to Use' };
  document.getElementById('topbarTitle').textContent = titles[id] || id;

  if (id === 'reminders') renderFullReminders();
  if (window.innerWidth < 768) toggleSidebar();
}

/* ── Pakistan Time ── */
function updateClock() {
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Karachi',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true
  });
  const t = fmt.format(new Date());
  document.getElementById('pkTime').textContent = t;
  document.getElementById('statTime').textContent = t;
}

/* ── Greeting ── */
function setGreeting() {
  const h = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Karachi' })).getHours();
  const g = h < 12 ? 'Good Morning ☀️' : h < 17 ? 'Good Afternoon 🌤' : h < 21 ? 'Good Evening 🌆' : 'Good Night 🌙';
  const el = document.getElementById('heroGreeting');
  if (el) el.textContent = g;
}

/* ── Bot Status ── */
async function checkStatus() {
  try {
    const r = await fetch('/api/stats', { signal: AbortSignal.timeout(5000) });
    const d = await r.json();
    const online = d.status === 'online';

    // Stat card
    document.getElementById('statStatus').innerHTML = online
      ? '<span class="dot online"></span><span class="online-text">Online</span>'
      : '<span class="dot offline"></span><span class="offline-text">Offline</span>';

    // Sidebar
    const sdot = document.getElementById('sidebarDot');
    const stext = document.getElementById('sidebarStatusText');
    sdot.className = 'sdot' + (online ? ' is-online' : '');
    stext.textContent = online ? 'Online' : 'Offline';

    return d;
  } catch {
    document.getElementById('statStatus').innerHTML =
      '<span class="dot offline"></span><span class="offline-text">Offline</span>';
    document.getElementById('sidebarDot').className = 'sdot';
    document.getElementById('sidebarStatusText').textContent = 'Offline';
    return null;
  }
}

/* ── Cache for reminders ── */
let _reminders = [];

/* ── Load All Data ── */
async function loadAll() {
  const data = await checkStatus();
  _reminders = data?.reminders || [];
  const count = _reminders.length;

  document.getElementById('statCount').textContent = count;
  document.getElementById('navCount').textContent = count;

  renderDashboardReminders();
}

/* ── Render in dashboard panel ── */
function renderDashboardReminders() {
  const el = document.getElementById('remindersList');
  if (!el) return;
  if (!_reminders.length) {
    el.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔔</div>
        <div class="empty-title">No active reminders</div>
        <div class="empty-sub">Set one using the form or send a WhatsApp message</div>
      </div>`;
    return;
  }
  el.innerHTML = _reminders.map(r => buildReminderCard(r)).join('');
}

/* ── Render in full view ── */
function renderFullReminders() {
  const el = document.getElementById('remindersFullList');
  if (!el) return;
  if (!_reminders.length) {
    el.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔔</div>
        <div class="empty-title">No active reminders</div>
        <div class="empty-sub">Set one using the form or send a WhatsApp message</div>
      </div>`;
    return;
  }
  el.innerHTML = _reminders.map(r => buildReminderCard(r)).join('');
}

function buildReminderCard(r) {
  const jobId   = r.id || '';
  const isCall  = jobId.toLowerCase().includes('call');
  const parts   = jobId.split('_');
  const taskRaw = parts.length > 3 ? parts.slice(1, -2).join(' ') : jobId;
  const task    = taskRaw.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const via     = isCall ? '📞 Phone Call' : '💬 WhatsApp';

  let timeStr = r.next_run || '';
  try {
    const dt = new Date(r.next_run);
    timeStr = new Intl.DateTimeFormat('en-US', {
      timeZone: 'Asia/Karachi',
      weekday: 'short', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', hour12: true
    }).format(dt);
  } catch {}

  return `
  <div class="r-item">
    <div>
      <div class="r-task">${task}</div>
      <div class="r-time">⏰ ${timeStr}</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0">
      <span class="r-badge">PENDING</span>
      <span class="r-via">${via}</span>
    </div>
  </div>`;
}

/* ── Notify Type Toggle ── */
function selectType(type) {
  notifyType = type;
  document.getElementById('segMsg').classList.toggle('active', type === 'message');
  document.getElementById('segCall').classList.toggle('active', type === 'call');
}

/* ── Set Default Date ── */
function setDefaultDate() {
  const today = new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Karachi' });
  const el = document.getElementById('date');
  if (el) { el.value = today; el.min = today; }
}

/* ── Set Reminder ── */
async function setReminder() {
  const phone = (document.getElementById('phone')?.value || '').trim();
  const task  = (document.getElementById('task')?.value  || '').trim();
  const date  = document.getElementById('date')?.value;
  const time  = document.getElementById('time')?.value;
  const btn   = document.getElementById('ctaBtn');

  if (!task)  { showAlert('Please enter a task!', 'danger');        return; }
  if (!date)  { showAlert('Please select a date!', 'danger');       return; }
  if (!time)  { showAlert('Please select a time!', 'danger');       return; }
  if (!phone) { showAlert('Please enter a phone number!', 'danger');return; }

  const datetimeStr = `${date}T${time}:00`;
  const reminderDt  = new Date(datetimeStr);
  const nowPk       = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Karachi' }));

  if (reminderDt < nowPk) {
    showAlert('⚠️ That time has already passed! Please choose a future time.', 'danger');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span>Setting…</span>';

  try {
    const res  = await fetch('/api/reminder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone, task, datetime: datetimeStr, reminder_type: notifyType })
    });
    const data = await res.json();

    if (data.status === 'success') {
      showAlert('✅ Reminder set successfully! You\'ll receive a WhatsApp confirmation.', 'success');
      document.getElementById('task').value = '';
      setDefaultDate();
      document.getElementById('time').value = '08:00';
      await loadAll();
    } else {
      showAlert('❌ ' + (data.message || 'Something went wrong.'), 'danger');
    }
  } catch {
    showAlert('❌ Could not connect to the bot server. Make sure it\'s running.', 'danger');
  }

  btn.disabled = false;
  btn.innerHTML = 'Set Reminder <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
}

/* ── Beep Sound ── */
function playBeep(type = 'success') {
  try {
    const ctx  = new (window.AudioContext || window.webkitAudioContext)();
    const gain = ctx.createGain();
    gain.connect(ctx.destination);

    const notes = type === 'success'
      ? [{ f: 523, t: 0 }, { f: 659, t: 0.12 }, { f: 784, t: 0.24 }]  // C5 E5 G5
      : [{ f: 300, t: 0 }];

    notes.forEach(({ f, t }) => {
      const osc = ctx.createOscillator();
      osc.connect(gain);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(f, ctx.currentTime + t);
      gain.gain.setValueAtTime(0.25, ctx.currentTime + t);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + t + 0.3);
      osc.start(ctx.currentTime + t);
      osc.stop(ctx.currentTime + t + 0.3);
    });
  } catch (e) {
    console.warn('Audio not supported:', e);
  }
}

/* ── Browser Notification ── */
function requestNotificationPermission() {
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
  }
}

function showBrowserNotification(title, body) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, {
      body,
      icon: 'https://cdn.jsdelivr.net/npm/twemoji@14.0.2/assets/72x72/1f514.png',
      badge: 'https://cdn.jsdelivr.net/npm/twemoji@14.0.2/assets/72x72/1f514.png'
    });
  }
}

/* ── Show Alert ── */
function showAlert(msg, type) {
  const el = document.getElementById('formAlert');
  if (!el) return;
  el.textContent = msg;
  el.className = `alert ${type}`;
  clearTimeout(el._t);
  el._t = setTimeout(() => { el.className = 'alert hidden'; }, 5000);

  if (type === 'success') {
    playBeep('success');
    showBrowserNotification('🔔 Reminder Set!', 'Your reminder has been scheduled successfully.');
  } else {
    playBeep('error');
  }
}

/* ══════════════════════════════════════
   INIT
══════════════════════════════════════ */
loadTheme();
requestNotificationPermission();
setGreeting();
setDefaultDate();
loadAll();
updateClock();
setInterval(updateClock, 1000);
setInterval(loadAll, 30000);