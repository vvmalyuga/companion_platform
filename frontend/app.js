const apiBase = window.API_BASE || '/api';
const app = document.querySelector('#app');
const state = { companions: [], analytics: [] };
const cubeToken = window.CUBE_TOKEN || 'secret';

async function loadCompanions() {
  try {
    const response = await fetch(`${apiBase}/companions`);
    state.companions = await response.json();
  } catch {
    state.companions = [
      { companionId:'cmp-001', name:'Анна', city:'Москва', age:27, categories:['прогулки','музеи'], interests:['кофе'], pricePerHour:1200, rating:4.9, photoUrl:'' },
      { companionId:'cmp-002', name:'Илья', city:'Санкт-Петербург', age:31, categories:['спорт'], interests:['бег'], pricePerHour:950, rating:4.7, photoUrl:'' }
    ];
  }
}

function card(item) {
  return `<article class="card"><img src="${item.photoUrl || ''}" alt="${item.name}"><h3>${item.name}, ${item.age}</h3><p>${item.city} · ${item.categories.join(', ')}</p><p>⭐ ${item.rating} · ${item.pricePerHour} ₽/час</p><a class="pill" href="#/companion/${item.companionId}">Профиль →</a></article>`;
}

function renderHome() {
  app.innerHTML = `<section class="hero"><h1>Найдите компанию для прогулок, спорта и событий</h1><p>Light UI, бирюзовые акценты, персональные рекомендации и безопасные бронирования.</p><button onclick="location.hash='#/catalog'">Смотреть каталог</button></section><section class="grid">${state.companions.map(card).join('')}</section>`;
}

function renderCatalog() {
  app.innerHTML = `<section class="filters"><input id="city" placeholder="Город"><select id="category"><option value="">Все категории</option><option>прогулки</option><option>спорт</option><option>мероприятия</option></select></section><section id="cards" class="grid"></section>`;
  const draw = () => {
    const city = document.querySelector('#city').value.toLowerCase();
    const category = document.querySelector('#category').value.toLowerCase();
    document.querySelector('#cards').innerHTML = state.companions.filter(item => (!city || item.city.toLowerCase().includes(city)) && (!category || item.categories.join('|').toLowerCase().includes(category))).map(card).join('');
  };
  document.querySelector('#city').addEventListener('input', draw);
  document.querySelector('#category').addEventListener('change', draw);
  draw();
}

function renderProfile(id) {
  const item = state.companions.find(companion => companion.companionId === id) || state.companions[0];
  app.innerHTML = `<section class="grid"><article class="card"><img src="${item.photoUrl || ''}" alt="${item.name}"><h2>${item.name}</h2><p>${item.city}, интересы: ${item.interests.join(', ')}</p><p>Отзывы: ⭐ ${item.rating}</p><button onclick="location.hash='#/booking/${item.companionId}'">Забронировать</button></article></section>`;
}

function renderBooking(id) {
  app.innerHTML = `<section class="grid"><form class="panel"><h2>Бронирование ${id}</h2><input type="datetime-local" required><select><option>прогулки</option><option>спорт</option><option>общение</option></select><button type="button" onclick="alert('Заявка создана')">Подтвердить</button></form></section>`;
}

async function loadAnalytics() {
  try {
    const query = encodeURIComponent(JSON.stringify({ measures:['CompanionActivity.BookingCount','CompanionActivity.Revenue'], dimensions:['CompanionActivity.category'] }));
    const response = await fetch(`/cubejs-api/v1/load?query=${query}`, { headers: { Authorization: cubeToken } });
    const payload = await response.json();
    state.analytics = payload.data || [];
  } catch {
    state.analytics = [
      { 'CompanionActivity.category':'прогулки', 'CompanionActivity.BookingCount':'42', 'CompanionActivity.Revenue':'104000' },
      { 'CompanionActivity.category':'спорт', 'CompanionActivity.BookingCount':'27', 'CompanionActivity.Revenue':'58000' }
    ];
  }
}

function renderDashboard() {
  const rows = state.analytics.length ? state.analytics : [{ 'CompanionActivity.category':'прогулки', 'CompanionActivity.BookingCount':'42', 'CompanionActivity.Revenue':'104000' }];
  app.innerHTML = `<section class="grid"><div class="panel"><h2>Customer dashboard</h2><div class="metrics"><div class="metric">BookingCount<br><b>${rows.reduce((sum,row)=>sum+Number(row['CompanionActivity.BookingCount']||0),0)}</b></div><div class="metric">Revenue<br><b>${rows.reduce((sum,row)=>sum+Number(row['CompanionActivity.Revenue']||0),0)} ₽</b></div></div><div class="chart">${rows.map(row => `<i title="${row['CompanionActivity.category']}" class="bar" style="height:${Math.max(20, Number(row['CompanionActivity.BookingCount']||1)*2)}%"></i>`).join('')}</div></div><div class="panel"><h2>Companion dashboard</h2><p>Drill-down: нажмите категорию для перехода category → companion.</p>${rows.map(row => `<button onclick="location.hash='#/catalog'; setTimeout(()=>document.querySelector('#category').value='${row['CompanionActivity.category']}',0)">${row['CompanionActivity.category']} → companion</button>`).join(' ')}</div></section>`;
}

function renderLogin() { app.innerHTML = `<section class="grid"><form class="panel"><h2>Login</h2><input type="email" placeholder="email"><input type="password" placeholder="password"><button type="button">Войти</button></form></section>`; }

async function route() {
  if (!state.companions.length) await loadCompanions();
  const [path, id] = location.hash.replace('#/', '').split('/');
  if (!path) return renderHome();
  if (path === 'catalog') return renderCatalog();
  if (path === 'companion') return renderProfile(id);
  if (path === 'booking') return renderBooking(id);
  if (path === 'dashboard') { await loadAnalytics(); return renderDashboard(); }
  if (path === 'login') return renderLogin();
  renderHome();
}
window.addEventListener('hashchange', route);
route();
