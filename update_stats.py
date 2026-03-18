#!/usr/bin/env python3
import requests

WP_URL = "https://funfit.nu"
auth   = ("info@funfit.nu", "he5r rquj NMuD hXOU KSU2 5rZa")

r = requests.get(f"{WP_URL}/wp-json/wp/v2/pages/5477?context=edit", auth=auth)
content = r.json()["content"]["raw"]

NEW_STATS = """  <div class="ff-stats-grid">

    <div class="ff-stat-card">
      <h3>&#127942; Meest gewonnen (1e plaats)</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Monique</span><span class="stat-val">8&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Gaoya</span><span class="stat-val">6&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Gwen</span><span class="stat-val">5&times; gewonnen</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128100; Meest deelgenomen</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Dennis</span><span class="stat-val">38 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Stefan</span><span class="stat-val">37 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Sjaak</span><span class="stat-val">36 challenges</span></div>
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
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Shoulder Taps</span><span class="stat-val">Jorgen &bull; 340</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Deadhang</span><span class="stat-val">Kees &bull; 2:43</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Bench Press</span><span class="stat-val">Robert &bull; 80 KG</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Curve loopband</span><span class="stat-val">Rob &bull; 24,0 km/u</span></div>
    </div>

  </div>"""

start = content.rfind('<div class="ff-stats-grid">')
end   = content.find('<div class="ff-updated"', start)
print(f"Stats sectie: chars {start}–{end} ({end-start} chars)")

updated = content[:start] + NEW_STATS + "\n\n  " + content[end:]

r2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages/5477",
    auth=auth,
    json={"content": updated, "status": "draft"}
)
print("Status:", r2.status_code, "✓ Stats bijgewerkt" if r2.status_code == 200 else r2.text[:200])
