#!/usr/bin/env python3
import requests
import json

WP_URL = "https://funfit.nu"
WP_USER = "info@funfit.nu"
WP_APP_PASSWORD = "he5r rquj NMuD hXOU KSU2 5rZa"

headers = {"Content-Type": "application/json"}
auth = (WP_USER, WP_APP_PASSWORD)

# ─── Statistics (pre-calculated) ─────────────────────────────────────────────
# Meest gewonnen: Monique 4x, Peter 2x, Robert 2x
# Meest deelgenomen: Stefan 14x, Monique 12x, Jorgen 12x
# Highest scores hardcoded per challenge

html_content = """
<style>
:root {
  --ff-blue: #0081a3;
  --ff-dark: #005f78;
  --ff-light: #00a8d4;
  --ff-gold: #FFD700;
  --ff-silver: #C0C0C0;
  --ff-bronze: #CD7F32;
  --ff-white: #ffffff;
  --ff-bg: #006b88;
}

.ff-wrap {
  font-family: 'Segoe UI', Arial, sans-serif;
  background: var(--ff-blue);
  color: var(--ff-white);
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 12px;
}

/* ── Header ── */
.ff-header {
  text-align: center;
  padding: 30px 20px 20px;
}
.ff-header h1 {
  font-size: 2.2rem;
  margin: 0 0 8px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #fff;
}
.ff-header .live-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(0,0,0,0.25);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 0.85rem;
  margin-top: 6px;
}
.pulse-dot {
  width: 10px; height: 10px;
  background: #4eff91;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0%,100%{opacity:1;transform:scale(1);}
  50%{opacity:.4;transform:scale(1.4);}
}

/* ── Tabs ── */
.ff-tabs {
  display: flex;
  gap: 8px;
  margin: 24px 0 0;
}
.ff-tab-btn {
  flex: 1;
  padding: 12px;
  border: 2px solid rgba(255,255,255,0.4);
  border-radius: 8px 8px 0 0;
  background: rgba(0,0,0,0.2);
  color: rgba(255,255,255,0.7);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all .2s;
  letter-spacing: 0.5px;
}
.ff-tab-btn.active {
  background: rgba(255,255,255,0.15);
  color: #fff;
  border-bottom-color: transparent;
}
.ff-tab-btn:hover { background: rgba(255,255,255,0.12); }

.ff-tab-panel {
  display: none;
  background: rgba(0,0,0,0.2);
  border-radius: 0 0 12px 12px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top: none;
  padding: 20px;
  min-height: 120px;
}
.ff-tab-panel.active { display: block; }

/* ── Loading / Error ── */
.ff-loading {
  text-align: center;
  padding: 40px;
  color: rgba(255,255,255,0.7);
  font-size: 1.1rem;
}
.ff-error {
  background: rgba(255,60,60,0.25);
  border-radius: 8px;
  padding: 16px;
  color: #ffaaaa;
  text-align: center;
}

/* ── Leaderboard table ── */
.ff-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.ff-table th {
  background: rgba(0,0,0,0.3);
  padding: 10px 14px;
  text-align: left;
  font-size: 0.8rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.7);
}
.ff-table td {
  padding: 10px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  font-size: 0.95rem;
}
.ff-table tr:last-child td { border-bottom: none; }
.ff-table tr:hover td { background: rgba(255,255,255,0.05); }

/* ── Challenge name ── */
.ff-challenge-name {
  text-align: center;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  background: rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 12px 20px;
  margin-bottom: 20px;
  border-left: 4px solid rgba(255,255,255,0.5);
}

/* ── Podium ── */
.ff-podium {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 12px;
  margin: 20px 0 30px;
}
.podium-block {
  text-align: center;
  background: rgba(0,0,0,0.25);
  border-radius: 10px 10px 0 0;
  padding: 14px 20px 10px;
  min-width: 90px;
  animation: riseUp .6s ease both;
}
.podium-block.p1 { background: rgba(255,215,0,0.2); order: 2; min-height: 130px; }
.podium-block.p2 { background: rgba(192,192,192,0.15); order: 1; min-height: 100px; }
.podium-block.p3 { background: rgba(205,127,50,0.15); order: 3; min-height: 80px; }
@keyframes riseUp {
  from { transform: translateY(30px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}
.podium-medal { font-size: 1.8rem; }
.podium-name { font-weight: 700; font-size: 0.9rem; margin-top: 6px; }
.podium-score { font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 2px; }
.pos-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  margin-right: 6px;
}
.pos-1 { background: rgba(255,215,0,0.3); color: var(--ff-gold); }
.pos-2 { background: rgba(192,192,192,0.3); color: var(--ff-silver); }
.pos-3 { background: rgba(205,127,50,0.3); color: var(--ff-bronze); }

.asterisk-note {
  font-size: 0.78rem;
  color: rgba(255,255,255,0.55);
  margin-top: 14px;
  padding: 10px;
  background: rgba(0,0,0,0.15);
  border-radius: 6px;
}

/* ── Section headers ── */
.ff-section-title {
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 40px 0 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(255,255,255,0.2);
  color: #fff;
}

/* ── Accordion ── */
.ff-accordion { margin-top: 8px; }
.ff-acc-item {
  background: rgba(0,0,0,0.2);
  border-radius: 8px;
  margin-bottom: 8px;
  overflow: hidden;
}
.ff-acc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  cursor: pointer;
  user-select: none;
  transition: background .2s;
}
.ff-acc-header:hover { background: rgba(255,255,255,0.08); }
.ff-acc-header-left { display: flex; align-items: center; gap: 12px; }
.ff-acc-num {
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700;
}
.ff-acc-title { font-weight: 600; font-size: 0.95rem; }
.ff-acc-date { font-size: 0.78rem; color: rgba(255,255,255,0.55); }
.ff-acc-arrow {
  transition: transform .3s;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.6);
}
.ff-acc-item.open .ff-acc-arrow { transform: rotate(180deg); }
.ff-acc-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height .35s ease;
}
.ff-acc-inner { padding: 0 18px 18px; }
.ff-acc-list { list-style: none; padding: 0; margin: 0; }
.ff-acc-list li {
  display: flex;
  align-items: center;
  padding: 7px 0;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  font-size: 0.88rem;
}
.ff-acc-list li:last-child { border-bottom: none; }
.acc-rank { min-width: 32px; font-weight: 700; color: rgba(255,255,255,0.5); font-size: 0.8rem; }
.acc-name { flex: 1; }
.acc-score { font-variant-numeric: tabular-nums; font-size: 0.85rem; color: rgba(255,255,255,0.75); }

/* ── Statistics ── */
.ff-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 8px;
}
.ff-stat-card {
  background: rgba(0,0,0,0.2);
  border-radius: 10px;
  padding: 18px;
}
.ff-stat-card h3 {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255,255,255,0.6);
  margin: 0 0 14px;
}
.stat-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 0;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  font-size: 0.9rem;
}
.stat-row:last-child { border-bottom: none; }
.stat-medal { font-size: 1.1rem; }
.stat-name { flex: 1; font-weight: 600; }
.stat-val { font-size: 0.82rem; color: rgba(255,255,255,0.7); }

/* ── Last updated ── */
.ff-updated {
  text-align: center;
  font-size: 0.78rem;
  color: rgba(255,255,255,0.45);
  margin-top: 30px;
  padding-top: 16px;
  border-top: 1px solid rgba(255,255,255,0.1);
}

/* ── Mobile ── */
@media(max-width:600px){
  .ff-header h1 { font-size: 1.5rem; }
  .ff-podium { gap: 8px; }
  .podium-block { min-width: 70px; padding: 10px 12px 8px; }
  .ff-stats-grid { grid-template-columns: 1fr; }
  .ff-table th, .ff-table td { padding: 8px 10px; }
}
</style>

<div class="ff-wrap">

  <!-- Header -->
  <div class="ff-header">
    <h1>&#127942; Challenge van de Week</h1>
    <p style="margin:4px 0 0;opacity:.8;font-size:.95rem;">Wie gaat er met de eer strijken?</p>
    <div class="live-badge">
      <span class="pulse-dot"></span>
      Live stand wordt elke dag ververst
    </div>
  </div>

  <!-- Live Leaderboard -->
  <div class="ff-tabs">
    <button class="ff-tab-btn active" onclick="ffShowTab('mannen',this)">&#9794; Mannen</button>
    <button class="ff-tab-btn" onclick="ffShowTab('vrouwen',this)">&#9792; Vrouwen</button>
  </div>

  <div id="ff-panel-mannen" class="ff-tab-panel active">
    <div class="ff-loading">&#8987; Live stand laden&hellip;</div>
  </div>
  <div id="ff-panel-vrouwen" class="ff-tab-panel">
    <div class="ff-loading">&#8987; Live stand laden&hellip;</div>
  </div>

  <!-- Historical Archive -->
  <div class="ff-section-title">&#128196; Challenge Archief</div>
  <div class="ff-accordion" id="ff-archief">

    <!-- 14: Lunge Challenge -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">14</span>
          <div><div class="ff-acc-title">Lunge Challenge (50x)</div><div class="ff-acc-date">29 aug 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">Snelste tijd wint (laagste = beter)</p>
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Deborah</span><span class="acc-score">122s</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Gwen</span><span class="acc-score">140s</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Jennifer</span><span class="acc-score">148s</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Rob</span><span class="acc-score">156s</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Ruud</span><span class="acc-score">157s</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Cynthia</span><span class="acc-score">158s</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Cathy</span><span class="acc-score">161s</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Dennis</span><span class="acc-score">163s</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Sven</span><span class="acc-score">168s</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Rene</span><span class="acc-score">169s</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Jorgen</span><span class="acc-score">172s</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Dyonne</span><span class="acc-score">173s</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Monique</span><span class="acc-score">173s</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Gaoya</span><span class="acc-score">176s</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Tim</span><span class="acc-score">180s</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Stefan</span><span class="acc-score">182s</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Ad</span><span class="acc-score">202s</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Kees</span><span class="acc-score">204s</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Britt</span><span class="acc-score">215s</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Peter</span><span class="acc-score">218s</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Minou</span><span class="acc-score">225s</span></li>
            <li><span class="acc-rank">22</span><span class="acc-name">Sjaak</span><span class="acc-score">233s</span></li>
            <li><span class="acc-rank">23</span><span class="acc-name">Pieter</span><span class="acc-score">234s</span></li>
            <li><span class="acc-rank">24</span><span class="acc-name">Aldo</span><span class="acc-score">235s</span></li>
            <li><span class="acc-rank">25</span><span class="acc-name">Petra</span><span class="acc-score">242s</span></li>
            <li><span class="acc-rank">26</span><span class="acc-name">Bente</span><span class="acc-score">293s</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 13: Bring Sally up Lunge -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">13</span>
          <div><div class="ff-acc-title">Bring Sally Up Lunge</div><div class="ff-acc-date">12 aug 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">Langste tijd wint &mdash; 6:46 = volledig volgehouden</p>
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Sjaak</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Ad</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Manon</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Gwen</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Robert</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Brit</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Monique</span><span class="acc-score">6:46 &#127942;</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Rene</span><span class="acc-score">5:57</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Kees</span><span class="acc-score">5:31</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Stefan</span><span class="acc-score">5:30</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Dyonne</span><span class="acc-score">4:53</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Aldo</span><span class="acc-score">4:50</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Petra</span><span class="acc-score">4:13</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Pieter</span><span class="acc-score">3:46</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Bente</span><span class="acc-score">3:39</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Dennis</span><span class="acc-score">3:23</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Jeroen</span><span class="acc-score">2:56</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Cynthia</span><span class="acc-score">2:02</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Pascal</span><span class="acc-score">1:44</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Danny</span><span class="acc-score">1:31</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 12: Kettlebell v-sit -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">12</span>
          <div><div class="ff-acc-title">Kettlebell V-Sit Static Hold</div><div class="ff-acc-date">8 aug 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 6px">Twee gewichtscategorieën</p>
          <p style="font-size:.85rem;font-weight:700;margin:10px 0 4px">4 KG</p>
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Cynthia</span><span class="acc-score">184s</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Manon</span><span class="acc-score">121s</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Dyonne</span><span class="acc-score">89s</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Marije</span><span class="acc-score">85s</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Monique</span><span class="acc-score">80s</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Brit</span><span class="acc-score">52s</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Petra</span><span class="acc-score">46s</span></li>
          </ul>
          <p style="font-size:.85rem;font-weight:700;margin:14px 0 4px">6 KG</p>
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Danny</span><span class="acc-score">107s</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Pascal</span><span class="acc-score">99s</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Aldo</span><span class="acc-score">88s</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Peter</span><span class="acc-score">85s</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Frank</span><span class="acc-score">69s</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Ad</span><span class="acc-score">67s</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Rene</span><span class="acc-score">61s</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Sjaak</span><span class="acc-score">55s</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Stefan</span><span class="acc-score">53s</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Dennis</span><span class="acc-score">51s</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Jorgen</span><span class="acc-score">44s</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Robert</span><span class="acc-score">40s</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Kees</span><span class="acc-score">37s</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Sven</span><span class="acc-score">35s</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 11: Bosu Balance Squat -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">11</span>
          <div><div class="ff-acc-title">Bosu Balance Squat (100 sec)</div><div class="ff-acc-date">1 aug 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Peter</span><span class="acc-score">83x</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Rob</span><span class="acc-score">82x</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Monique</span><span class="acc-score">82x</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Cathy</span><span class="acc-score">80x</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Ruud</span><span class="acc-score">75x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Kees</span><span class="acc-score">74x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Frank</span><span class="acc-score">74x</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Marije</span><span class="acc-score">72x</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Minou</span><span class="acc-score">69x</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Jorgen</span><span class="acc-score">69x</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Bente</span><span class="acc-score">67x</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Stefan</span><span class="acc-score">65x</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Dennis</span><span class="acc-score">63x</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Aldo</span><span class="acc-score">62x</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Cynthia</span><span class="acc-score">61x</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Jeanet</span><span class="acc-score">60x</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Gwen</span><span class="acc-score">59x</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Pieter</span><span class="acc-score">55x</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Lotte</span><span class="acc-score">54x</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Dyonne</span><span class="acc-score">53x</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Sjaak</span><span class="acc-score">50x</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Liesbeth</span><span class="acc-score">50x</span></li>
            <li><span class="acc-rank">23</span><span class="acc-name">Britt</span><span class="acc-score">46x</span></li>
            <li><span class="acc-rank">24</span><span class="acc-name">Petra</span><span class="acc-score">44x</span></li>
            <li><span class="acc-rank">25</span><span class="acc-name">Danny</span><span class="acc-score">42x</span></li>
            <li><span class="acc-rank">26</span><span class="acc-name">Esther</span><span class="acc-score">40x</span></li>
            <li><span class="acc-rank">27</span><span class="acc-name">Pascal</span><span class="acc-score">31x</span></li>
            <li><span class="acc-rank">28</span><span class="acc-name">Rene</span><span class="acc-score">29x</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 10: Bosu Balance Bal Gooien -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">10</span>
          <div><div class="ff-acc-title">Bosu Balance Bal Gooien</div><div class="ff-acc-date">30 jul 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Max</span><span class="acc-score">86x</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Jorgen</span><span class="acc-score">86x</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Stefan</span><span class="acc-score">78x</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Monique</span><span class="acc-score">65x</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Frank</span><span class="acc-score">64x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Lotte</span><span class="acc-score">60x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Peter</span><span class="acc-score">60x</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Cathy</span><span class="acc-score">58x</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Jeroen</span><span class="acc-score">58x</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Pieter</span><span class="acc-score">57x</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Marije</span><span class="acc-score">57x</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Dennis</span><span class="acc-score">56x</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Ruud</span><span class="acc-score">55x</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Sabrine</span><span class="acc-score">54x</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Bente</span><span class="acc-score">54x</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Rene</span><span class="acc-score">53x</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Petra</span><span class="acc-score">45x</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Lotte</span><span class="acc-score">44x</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Ad</span><span class="acc-score">44x</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Aldo</span><span class="acc-score">41x</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Danny</span><span class="acc-score">41x</span></li>
            <li><span class="acc-rank">22</span><span class="acc-name">Sjaak</span><span class="acc-score">36x</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 9: Bankdruk -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">9</span>
          <div><div class="ff-acc-title">Bankdruk Challenge</div><div class="ff-acc-date">22 jul 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Robert</span><span class="acc-score">160x</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Cathy</span><span class="acc-score">135x</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Marije</span><span class="acc-score">120x</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Ruud</span><span class="acc-score">115x</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Frank</span><span class="acc-score">110x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Monique</span><span class="acc-score">109x</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Stefan</span><span class="acc-score">106x</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Jorgen</span><span class="acc-score">103x</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Sabrine</span><span class="acc-score">103x</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Kees</span><span class="acc-score">103x</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Rene</span><span class="acc-score">100x</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Minou</span><span class="acc-score">100x</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Dennis</span><span class="acc-score">97x</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Aldo</span><span class="acc-score">94x</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Rob</span><span class="acc-score">94x</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Pieter</span><span class="acc-score">93x</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Cynthia</span><span class="acc-score">88x</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Danny</span><span class="acc-score">85x</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Sjaak</span><span class="acc-score">79x</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Britt</span><span class="acc-score">78x</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Ad</span><span class="acc-score">73x</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Bente</span><span class="acc-score">73x</span></li>
            <li><span class="acc-rank">23</span><span class="acc-name">Peter</span><span class="acc-score">72x</span></li>
            <li><span class="acc-rank">24</span><span class="acc-name">Petra</span><span class="acc-score">60x</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 8: Plank -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">8</span>
          <div><div class="ff-acc-title">Plank Challenge</div><div class="ff-acc-date">16 jul 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">Notatie: seconden+extra</p>
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Sylcia</span><span class="acc-score">220+12</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Monique</span><span class="acc-score">220+00</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Rob</span><span class="acc-score">200+72</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Ruud</span><span class="acc-score">200+10</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Lotte</span><span class="acc-score">190+04</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Manon</span><span class="acc-score">180+00</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Cathy</span><span class="acc-score">160+88</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Peter</span><span class="acc-score">150+86</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Jorgen</span><span class="acc-score">150+40</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Gwen</span><span class="acc-score">150+20</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Aldo</span><span class="acc-score">130+60</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Kees</span><span class="acc-score">110+80</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Frank</span><span class="acc-score">110+20</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Minou</span><span class="acc-score">100+60</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Rene</span><span class="acc-score">100+35</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Ad</span><span class="acc-score">100+22</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Sjaak</span><span class="acc-score">90+27</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Pieter</span><span class="acc-score">90+21</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Danny</span><span class="acc-score">80+65</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Brit</span><span class="acc-score">80+30</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Dennis</span><span class="acc-score">80+26</span></li>
            <li><span class="acc-rank">22</span><span class="acc-name">Petra</span><span class="acc-score">70+28</span></li>
            <li><span class="acc-rank">23</span><span class="acc-name">Dyonne</span><span class="acc-score">70+22</span></li>
            <li><span class="acc-rank">24</span><span class="acc-name">Pascal</span><span class="acc-score">70+14</span></li>
            <li><span class="acc-rank">25</span><span class="acc-name">Bente</span><span class="acc-score">50+29</span></li>
            <li><span class="acc-rank">26</span><span class="acc-name">Stefan</span><span class="acc-score">50+22</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 7: Skiën -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">7</span>
          <div><div class="ff-acc-title">Ski&euml;n over Halterbank</div><div class="ff-acc-date">28 jun 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Ruud</span><span class="acc-score">129x</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Jorgen</span><span class="acc-score">118x</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Cathy</span><span class="acc-score">112x</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Rob</span><span class="acc-score">106x</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Jeanet</span><span class="acc-score">98x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Aldo</span><span class="acc-score">96x</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Monique</span><span class="acc-score">95x</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Frank</span><span class="acc-score">95x</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Pieter</span><span class="acc-score">93x</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Jos</span><span class="acc-score">91x</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Marije</span><span class="acc-score">89x</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Britt</span><span class="acc-score">78x</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Lotte</span><span class="acc-score">74x</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Tim</span><span class="acc-score">74x</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Bente</span><span class="acc-score">68x</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Stefan</span><span class="acc-score">62x</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Sabrine</span><span class="acc-score">60x</span></li>
            <li><span class="acc-rank">&mdash;</span><span class="acc-name">Peter</span><span class="acc-score">DNF</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 6: Dippen -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">6</span>
          <div><div class="ff-acc-title">180 sec Dippen</div><div class="ff-acc-date">31 mei 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Peter</span><span class="acc-score">180 reps</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Rob</span><span class="acc-score">174</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Kees</span><span class="acc-score">147</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Marije</span><span class="acc-score">146</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Ruud</span><span class="acc-score">144</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Cathy</span><span class="acc-score">143</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Stefan</span><span class="acc-score">122</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Rene</span><span class="acc-score">120</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Benthe</span><span class="acc-score">118</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Pieter</span><span class="acc-score">117</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Jorgen</span><span class="acc-score">115</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Monique</span><span class="acc-score">108</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Esther</span><span class="acc-score">106</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Jeanet</span><span class="acc-score">100</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Sabrine</span><span class="acc-score">96</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Lotte</span><span class="acc-score">94</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Minou</span><span class="acc-score">91</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Bas</span><span class="acc-score">90</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Sjaak</span><span class="acc-score">82</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Petra</span><span class="acc-score">67</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 5: Bosu Balance -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">5</span>
          <div><div class="ff-acc-title">Bosu Balance</div><div class="ff-acc-date">26 mei 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Minou</span><span class="acc-score">240s &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Marije</span><span class="acc-score">240s &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Monique</span><span class="acc-score">240s &#127942;</span></li>
            <li><span class="acc-rank">1</span><span class="acc-name">Gaoya</span><span class="acc-score">240s &#127942;</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Cynthia</span><span class="acc-score">217s</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Peter</span><span class="acc-score">203s</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Sabrine</span><span class="acc-score">189s</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Rob</span><span class="acc-score">188s</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Liset</span><span class="acc-score">167s</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Ruud</span><span class="acc-score">152s</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Lotte</span><span class="acc-score">125s</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Jorgen</span><span class="acc-score">124s</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Jeanet</span><span class="acc-score">109s</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Benthe</span><span class="acc-score">87s</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Esther</span><span class="acc-score">77s</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Frank</span><span class="acc-score">76s</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Stefan</span><span class="acc-score">70s</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Max</span><span class="acc-score">69s</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Wendy</span><span class="acc-score">69s</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Dennis</span><span class="acc-score">57s</span></li>
            <li><span class="acc-rank">21</span><span class="acc-name">Bas</span><span class="acc-score">54s</span></li>
            <li><span class="acc-rank">22</span><span class="acc-name">Rene</span><span class="acc-score">53s</span></li>
            <li><span class="acc-rank">23</span><span class="acc-name">Robert</span><span class="acc-score">44s</span></li>
            <li><span class="acc-rank">24</span><span class="acc-name">Pieter</span><span class="acc-score">37s</span></li>
            <li><span class="acc-rank">25</span><span class="acc-name">Kees</span><span class="acc-score">35s</span></li>
            <li><span class="acc-rank">26</span><span class="acc-name">Petra</span><span class="acc-score">21s</span></li>
            <li><span class="acc-rank">27</span><span class="acc-name">Sjako</span><span class="acc-score">15s</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 4: Horizontal Pull Ups -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">4</span>
          <div><div class="ff-acc-title">Horizontal Pull Ups Challenge</div><div class="ff-acc-date">2 mei 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Monique</span><span class="acc-score">48x</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Gaoya</span><span class="acc-score">47x</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Robert</span><span class="acc-score">39x</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Frank</span><span class="acc-score">38x</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Aldo</span><span class="acc-score">33x</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Rene</span><span class="acc-score">30x</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Ruud</span><span class="acc-score">28x</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Marije</span><span class="acc-score">28x</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Jorgen</span><span class="acc-score">27x</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Rob</span><span class="acc-score">27x</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Jeanet</span><span class="acc-score">21x</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Lotte</span><span class="acc-score">21x</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Sabrien</span><span class="acc-score">20x</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Sjaak</span><span class="acc-score">18x</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Dennis</span><span class="acc-score">16x</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Stefan</span><span class="acc-score">10x</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 3: 500m Row -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">3</span>
          <div><div class="ff-acc-title">500m Row Challenge</div><div class="ff-acc-date">11 mrt 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">Snelste tijd wint (laagste = beter)</p>
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Rob</span><span class="acc-score">1:40</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Jorgen</span><span class="acc-score">1:41</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Stefan</span><span class="acc-score">1:42</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Pieter</span><span class="acc-score">1:44</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Dennis</span><span class="acc-score">1:46</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Peter</span><span class="acc-score">1:46</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Sven</span><span class="acc-score">1:46</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Ruud</span><span class="acc-score">1:47</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Sjaak</span><span class="acc-score">1:47</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Aldo</span><span class="acc-score">1:48</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Kees</span><span class="acc-score">1:49</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Minou</span><span class="acc-score">1:52</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Rene</span><span class="acc-score">1:56</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Marije</span><span class="acc-score">1:56</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Wendy</span><span class="acc-score">1:59</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Petra</span><span class="acc-score">2:07</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Jeanet</span><span class="acc-score">2:14</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 2: Wallsit -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">2</span>
          <div><div class="ff-acc-title">Wallsit Challenge</div><div class="ff-acc-date">28 feb 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Gaoya</span><span class="acc-score">490s</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Wendy</span><span class="acc-score">310s</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Kees</span><span class="acc-score">305s</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Jeanet</span><span class="acc-score">246s</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Minou</span><span class="acc-score">240s</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Max</span><span class="acc-score">210s</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Peter</span><span class="acc-score">198s</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Jorgen</span><span class="acc-score">197s</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Cynthia</span><span class="acc-score">190s</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Ruud</span><span class="acc-score">165s</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Rob</span><span class="acc-score">150s</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Peet</span><span class="acc-score">148s</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Sjaak</span><span class="acc-score">134s</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Monique</span><span class="acc-score">128s</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Pieter</span><span class="acc-score">127s</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Britt</span><span class="acc-score">124s</span></li>
            <li><span class="acc-rank">17</span><span class="acc-name">Aldo</span><span class="acc-score">123s</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Stefan</span><span class="acc-score">81s</span></li>
            <li><span class="acc-rank">19</span><span class="acc-name">Rene</span><span class="acc-score">67s</span></li>
            <li><span class="acc-rank">20</span><span class="acc-name">Dennis</span><span class="acc-score">63s</span></li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 1: Paalhang -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">1</span>
          <div><div class="ff-acc-title">Paalhang Challenge</div><div class="ff-acc-date">5 feb 2022</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          <ul class="ff-acc-list">
            <li><span class="acc-rank">1</span><span class="acc-name">Jennifer</span><span class="acc-score">257s</span></li>
            <li><span class="acc-rank">2</span><span class="acc-name">Monique</span><span class="acc-score">193s</span></li>
            <li><span class="acc-rank">3</span><span class="acc-name">Ruud</span><span class="acc-score">163s</span></li>
            <li><span class="acc-rank">4</span><span class="acc-name">Aldo</span><span class="acc-score">150s</span></li>
            <li><span class="acc-rank">5</span><span class="acc-name">Rob</span><span class="acc-score">126s</span></li>
            <li><span class="acc-rank">6</span><span class="acc-name">Tim</span><span class="acc-score">101s</span></li>
            <li><span class="acc-rank">7</span><span class="acc-name">Frank</span><span class="acc-score">89s</span></li>
            <li><span class="acc-rank">8</span><span class="acc-name">Stefan</span><span class="acc-score">85s</span></li>
            <li><span class="acc-rank">9</span><span class="acc-name">Sjaak</span><span class="acc-score">80s</span></li>
            <li><span class="acc-rank">10</span><span class="acc-name">Peter</span><span class="acc-score">78s</span></li>
            <li><span class="acc-rank">11</span><span class="acc-name">Jorgen</span><span class="acc-score">69s</span></li>
            <li><span class="acc-rank">12</span><span class="acc-name">Desiree</span><span class="acc-score">63s</span></li>
            <li><span class="acc-rank">13</span><span class="acc-name">Pieter</span><span class="acc-score">61s</span></li>
            <li><span class="acc-rank">14</span><span class="acc-name">Kees</span><span class="acc-score">60s</span></li>
            <li><span class="acc-rank">15</span><span class="acc-name">Sabrine</span><span class="acc-score">35s</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Dennis</span><span class="acc-score">33s</span></li>
            <li><span class="acc-rank">16</span><span class="acc-name">Jeanet</span><span class="acc-score">33s</span></li>
            <li><span class="acc-rank">18</span><span class="acc-name">Tante Brit</span><span class="acc-score">0,01s</span></li>
          </ul>
        </div>
      </div>
    </div>

  </div><!-- /accordion -->

  <!-- Statistics -->
  <div class="ff-section-title">&#128202; Statistieken (archief)</div>
  <div class="ff-stats-grid">

    <div class="ff-stat-card">
      <h3>&#127942; Meest gewonnen (1e plaats)</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Monique</span><span class="stat-val">4&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Peter</span><span class="stat-val">2&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Robert</span><span class="stat-val">2&times; gewonnen</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128100; Meest deelgenomen</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Stefan</span><span class="stat-val">14 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Monique</span><span class="stat-val">12 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Jorgen</span><span class="stat-val">12 challenges</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128293; Records per challenge</h3>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Paalhang</span><span class="stat-val">Jennifer &bull; 257s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Wallsit</span><span class="stat-val">Gaoya &bull; 490s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">500m Row</span><span class="stat-val">Rob &bull; 1:40</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Pull Ups</span><span class="stat-val">Monique &bull; 48x</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Dippen</span><span class="stat-val">Peter &bull; 180 reps</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Ski&euml;n</span><span class="stat-val">Ruud &bull; 129x</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Bankdruk</span><span class="stat-val">Robert &bull; 160x</span></div>
    </div>

  </div>

  <div class="ff-updated" id="ff-updated-at">Stand geladen op: &hellip;</div>

</div><!-- /ff-wrap -->

<script>
(function(){
  var BASE_URL = 'https://docs.google.com/spreadsheets/d/1KG5cdYOjRxKoVVc9n4xQ91qkPPO7tBrZ/gviz/tq?tqx=out:json';

  function ffShowTab(tab, btn) {
    document.querySelectorAll('.ff-tab-btn').forEach(function(b){ b.classList.remove('active'); });
    document.querySelectorAll('.ff-tab-panel').forEach(function(p){ p.classList.remove('active'); });
    btn.classList.add('active');
    document.getElementById('ff-panel-' + tab).classList.add('active');
  }
  window.ffShowTab = ffShowTab;

  function ffToggle(header) {
    var item = header.closest('.ff-acc-item');
    var body = item.querySelector('.ff-acc-body');
    var isOpen = item.classList.contains('open');
    item.classList.toggle('open', !isOpen);
    body.style.maxHeight = isOpen ? '0' : body.scrollHeight + 'px';
  }
  window.ffToggle = ffToggle;

  function parseGviz(text) {
    // Strip Google's JSONP wrapper
    var json = text.replace(/^[^{]*/, '').replace(/[^}]*$/, '');
    try { return JSON.parse(json); } catch(e) { return null; }
  }

  function buildTable(rows, panel, challengeName) {
    if (!rows || rows.length === 0) {
      panel.innerHTML = '<div class="ff-error">Geen data beschikbaar.</div>';
      return;
    }

    // Challenge name header
    var nameHtml = challengeName
      ? '<div class="ff-challenge-name">' + challengeName + '</div>'
      : '';

    // Podium (top 3)
    var podiumData = rows.slice(0, 3);
    var podiumHtml = '<div class="ff-podium">';
    var medals = ['&#129351;','&#129352;','&#129353;'];
    var classes = ['p1','p2','p3'];
    for (var i = 0; i < podiumData.length; i++) {
      var r = podiumData[i];
      var pos = r[0] || (i+1);
      var name = r[1] || '';
      var score = r[2] || '';
      var hasAsterisk = name.indexOf('*') !== -1;
      var displayName = name.replace('*','');
      podiumHtml += '<div class="podium-block ' + classes[i] + '">';
      podiumHtml += '<div class="podium-medal">' + medals[i] + '</div>';
      podiumHtml += '<div class="podium-name">' + displayName + (hasAsterisk ? ' <sup>*</sup>' : '') + '</div>';
      podiumHtml += '<div class="podium-score">' + score + '</div>';
      podiumHtml += '</div>';
    }
    podiumHtml += '</div>';

    // Full table
    var tableHtml = '<table class="ff-table"><thead><tr><th>#</th><th>Naam</th><th>Score</th></tr></thead><tbody>';
    for (var j = 0; j < rows.length; j++) {
      var row = rows[j];
      var pos2 = row[0] !== undefined ? row[0] : (j+1);
      var name2 = row[1] || '';
      var score2 = row[2] || '';
      var hasAst = name2.indexOf('*') !== -1;
      var dispName = name2.replace('*','');
      var posClass = pos2 == 1 ? 'pos-1' : pos2 == 2 ? 'pos-2' : pos2 == 3 ? 'pos-3' : '';
      tableHtml += '<tr>';
      tableHtml += '<td><span class="pos-badge ' + posClass + '">' + pos2 + '</span></td>';
      tableHtml += '<td>' + dispName + (hasAst ? ' <sup style="color:rgba(255,255,255,.6)">*</sup>' : '') + '</td>';
      tableHtml += '<td>' + score2 + '</td>';
      tableHtml += '</tr>';
    }
    tableHtml += '</tbody></table>';

    var hasAsterisks = rows.some(function(r){ return r[1] && r[1].indexOf('*') !== -1; });
    var note = hasAsterisks ? '<div class="asterisk-note">* Heeft met afwijkend gewicht gewerkt &mdash; telt niet mee in de offici&euml;le uitslag.</div>' : '';

    panel.innerHTML = nameHtml + podiumHtml + tableHtml + note;
  }

  function loadSheet(sheetName, panelId) {
    var panel = document.getElementById(panelId);
    var url = BASE_URL + '&sheet=' + encodeURIComponent(sheetName);

    fetch(url)
      .then(function(res){ return res.text(); })
      .then(function(text){
        var data = parseGviz(text);
        if (!data || !data.table) {
          panel.innerHTML = '<div class="ff-error">Kon data niet laden. Probeer later opnieuw.</div>';
          return;
        }
        // Row 0 = challenge name, row 1 = header (Naam/Score), row 2+ = data
        var allRows = data.table.rows || [];
        var challengeName = '';
        if (allRows[0] && allRows[0].c) {
          var nameCell = allRows[0].c.find(function(c){ return c && c.v; });
          if (nameCell) challengeName = String(nameCell.v);
        }
        var rows = allRows.slice(2).map(function(row){
          if (!row.c) return [null,null,null];
          return row.c.map(function(cell){ return cell ? cell.v : null; });
        }).filter(function(r){ return r[1]; }); // skip challenge name + header + empty rows
        buildTable(rows, panel, challengeName);
        var now = new Date();
        document.getElementById('ff-updated-at').textContent =
          'Stand geladen op: ' + now.toLocaleDateString('nl-NL') + ' om ' + now.toLocaleTimeString('nl-NL', {hour:'2-digit',minute:'2-digit'});
      })
      .catch(function(){
        panel.innerHTML = '<div class="ff-error">Fout bij laden van live data. Controleer de verbinding.</div>';
      });
  }

  function loadAll() {
    loadSheet('Mannen', 'ff-panel-mannen');
    loadSheet('Vrouwen', 'ff-panel-vrouwen');
  }

  // Initial load
  loadAll();

  // Auto-refresh every 24 hours
  setInterval(loadAll, 24 * 60 * 60 * 1000);
})();
</script>
"""

page_data = {
    "title": "Challenge van de Week – Live Leaderboard",
    "slug": "challenge-van-de-week",
    "content": html_content,
    "status": "draft",
    "meta": {
        "description": "Live leaderboard van de FunFit wekelijkse challenge. Bekijk de tussenstand voor mannen en vrouwen, plus het historisch archief van alle challenges."
    }
}

print("Posting page to WordPress...")
response = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages",
    headers=headers,
    auth=auth,
    json=page_data
)

print(f"Status: {response.status_code}")
if response.status_code in (200, 201):
    data = response.json()
    print(f"✓ Pagina aangemaakt!")
    print(f"  ID:     {data['id']}")
    print(f"  Slug:   {data['slug']}")
    print(f"  Status: {data['status']}")
    print(f"  Preview URL: {data.get('link','')}")
    print(f"  Edit URL: {WP_URL}/wp-admin/post.php?post={data['id']}&action=edit")
else:
    print(f"Fout: {response.text[:500]}")
