#!/usr/bin/env python3
"""Voegt challenges #55–87 toe aan de WordPress leaderboard pagina."""
import requests

WP_URL  = "https://funfit.nu"
auth    = ("info@funfit.nu", "he5r rquj NMuD hXOU KSU2 5rZa")
PAGE_ID = 5477

# ── Helpers ──────────────────────────────────────────────────────────────────
def li(rank, name, score):
    return (f'<li><span class="acc-rank">{rank}</span>'
            f'<span class="acc-name">{name}</span>'
            f'<span class="acc-score">{score}</span></li>')
def ul(items): return '<ul class="ff-acc-list">' + "".join(items) + "</ul>"
def cat(label): return f'<p style="font-size:.85rem;font-weight:700;margin:14px 0 4px">{label}</p>'
def note(text): return f'<p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">{text}</p>'
def acc(num, title, date, inner):
    return f"""
    <!-- {num}: {title} -->
    <div class="ff-acc-item">
      <div class="ff-acc-header" onclick="ffToggle(this)">
        <div class="ff-acc-header-left">
          <span class="ff-acc-num">{num}</span>
          <div><div class="ff-acc-title">{title}</div><div class="ff-acc-date">{date}</div></div>
        </div>
        <span class="ff-acc-arrow">&#9660;</span>
      </div>
      <div class="ff-acc-body"><div class="ff-acc-inner">{inner}</div></div>
    </div>"""

# ── #87 ───────────────────────────────────────────────────────────────────────
c87 = acc(87, "Slamball challenge (2 minuten)", "6 september 2024",
    note("Meeste herhalingen wint &mdash; Heren 16 KG &bull; Dames 10 KG") +
    cat("Heren") + ul([
        li(1,"Jorgen","52"), li(2,"Dennis B","50"), li(2,"Hilbert","50"), li(4,"Wouter","49"),
        li(5,"Max","48"), li(5,"Radboud","48"), li(7,"Stefan","46"), li(8,"Bram","45"),
        li(8,"Roderick","45"), li(8,"Dennis W","45"), li(11,"Pim","41"), li(11,"Robin H","41"),
        li(13,"Jeroen","39"), li(14,"Rene","38"), li(15,"Sjaak","36"), li(16,"Aldo","35"),
        li(17,"Frank B","29"), li(18,"Amresh","17"),
    ]) + cat("Dames") + ul([
        li(1,"Manon","67"), li(2,"Cynthia","60"), li(2,"Dyonne","60"), li(4,"Gaoya","59"),
        li(5,"Wendy","57"), li(6,"Vivian","54"), li(7,"Bente","52"), li(8,"Cathy","50"),
        li(8,"Janneke","50"), li(10,"Liesbeth","49"), li(11,"Marije","47"), li(12,"Fiona","45"),
        li(13,"Eef","41"), li(14,"Petra","34"), li(15,"Paula","33"),
    ])
)

# ── #86 ───────────────────────────────────────────────────────────────────────
c86 = acc(86, "Step plank push-ups (50x)", "29 augustus 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Bram","48s"), li(2,"Roderick","49s"), li(2,"Robert","49s"), li(4,"Koen","51s"),
        li(5,"Ruud","55s"), li(5,"Radboud","55s"), li(7,"Niels K.","56s"), li(8,"Rob","59s"),
        li(9,"Robin H.","60s"), li(10,"Elwin","65s"), li(11,"Sjaak","68s"), li(12,"Dennis B","69s"),
        li(13,"Aldo","70s"), li(13,"Frank Z.","70s"), li(15,"Frank M.","75s"), li(16,"Robin S.","77s"),
        li(17,"Richard","84s"), li(18,"Jeroen","91s"), li(19,"Pim","107s"),
    ]) + cat("Dames") + ul([
        li(1,"Anne","71s"), li(2,"Cynthia","73s"), li(3,"Bente","76s"), li(3,"Fiona","76s"),
        li(5,"Monica","79s"), li(6,"Vivian","84s"), li(6,"Charissa","84s"), li(8,"Eef","92s"),
    ])
)

# ── #85 ───────────────────────────────────────────────────────────────────────
c85 = acc(85, "Wall sit challenge", "22 augustus 2024",
    note("Langste tijd wint") +
    cat("Heren") + ul([
        li(1,"Ivan","323s"), li(2,"Elwin","313s"), li(3,"Niels K","266s"), li(4,"Peter","263s"),
        li(5,"Robert","240s"), li(6,"Richard","213s"), li(7,"Pim","204s"), li(8,"Radboud","193s"),
        li(9,"Jorgen","187s"), li(10,"Robin","180s"), li(11,"Wouter","165s"), li(12,"Frank B","139s"),
        li(13,"Koen","131s"), li(13,"Ruud","131s"), li(15,"Nic","120s"), li(15,"Stefan","120s"),
        li(15,"Dennis B","120s"), li(18,"Bram","117s"), li(19,"Roderick","114s"), li(20,"Udo","103s"),
        li(21,"Rob","102s"), li(22,"Sjaak","90s"), li(23,"Rene","83s"), li(24,"Ad","70s"),
    ]) + cat("Dames") + ul([
        li(1,"Gwen","426s"), li(2,"Manon","364s"), li(3,"Gaoya","360s"), li(4,"Lotte","334s"),
        li(5,"Paula","269s"), li(6,"Charissa","250s"), li(7,"Monica","196s"), li(8,"Dyonne","185s"),
        li(9,"Wendy","184s"), li(10,"Liesbeth","158s"), li(11,"Petra","157s"), li(12,"Cathy","155s"),
        li(13,"Anne","151s"), li(14,"Fiona","134s"), li(15,"Stefanie","123s"), li(16,"Gloria","118s"),
        li(17,"Marije","103s"), li(18,"Britt","92s"),
    ])
)

# ── #84 ───────────────────────────────────────────────────────────────────────
c84 = acc(84, "Assault bike (hoogste wattage)", "7 augustus 2024",
    note("Hoogste wattage wint") +
    cat("Heren") + ul([
        li(1,"Stefan","1278W"), li(2,"Mark","1245W"), li(3,"Jeroen","1147W"),
        li(4,"Robert","1115W"), li(4,"Stijn","1115W"), li(6,"Dennis","1082W"),
        li(7,"Jorgen","985W"), li(7,"Aldo","985W"), li(9,"Bram","857W"),
        li(10,"Frank","818W"), li(11,"Radboud","792W"), li(12,"Ad","739W"),
        li(12,"Sjaak","739W"), li(14,"Richard","679W"), li(15,"Roderick","676W"),
    ]) + cat("Dames") + ul([
        li(1,"Anne","655W &#127942;"), li(1,"Charissa","655W &#127942;"), li(1,"Bente","655W &#127942;"),
        li(4,"Kirsten","632W"), li(5,"Madou","616W"), li(6,"Cynthia","570W"), li(7,"Gloria","549W"),
    ])
)

# ── #83 ───────────────────────────────────────────────────────────────────────
c83 = acc(83, "Olympics triathlon challenge", "1 augustus 2024",
    note("Snelste tijd wint &mdash; 10 burpees + 100 sit-ups + rondje om het veld FC Lisse") +
    cat("Heren") + ul([
        li(1,"Robert","4:37"), li(2,"Bram","5:49"), li(3,"Dennis","5:53"), li(4,"Roderick","6:04"),
        li(5,"Sjaak","7:04"), li(6,"Robin","7:11"), li(7,"Hilbert","7:30"), li(8,"Arjan","9:26"),
        li(9,"Jeroen","10:32"),
    ]) + cat("Dames") + ul([
        li(1,"Charissa","5:45"), li(2,"Gloria","5:55"), li(3,"Anne","6:09"),
        li(4,"Paula","7:24"), li(5,"Janneke","7:30"),
    ])
)

# ── #82 ───────────────────────────────────────────────────────────────────────
c82 = acc(82, "Assault bike challenge (10 calorie&euml;n)", "24 juli 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Mark","10s"), li(2,"Robert","11s"), li(2,"Robert E","11s"), li(4,"Stefan","13s"),
        li(4,"Ruud","13s"), li(6,"Robin","14s"), li(7,"Bart","15s"), li(7,"Aldo","15s"),
        li(7,"Dennis","15s"), li(7,"Frank","15s"), li(7,"Kevin","15s"), li(7,"Pieter","15s"),
        li(13,"Dennis [2]","17s"), li(13,"Koen","17s"), li(13,"Bram","17s"), li(16,"Frank B","18s"),
        li(16,"Arjan","18s"), li(18,"AD","19s"), li(18,"Frank Z.","19s"), li(20,"Sjaak","20s"),
        li(21,"Udo","36s"),
    ]) + cat("Dames") + ul([
        li(1,"Wendy","17s"), li(2,"Vivian","19s"), li(3,"Dyonne","21s"), li(4,"Gaoya","22s"),
        li(4,"Gwen","22s"), li(6,"Cathy","23s"), li(6,"Manon","23s"), li(8,"Janneke","26s"),
        li(8,"Pascale","26s"), li(10,"Bente","27s"), li(11,"Mirthe","28s"), li(12,"Eef","30s"),
        li(13,"Fiona","31s"), li(13,"Charissa","31s"), li(15,"Gloria","33s"), li(16,"Paula","42s"),
    ])
)

# ── #81 ───────────────────────────────────────────────────────────────────────
c81 = acc(81, "Russian twist challenge (6 schijven)", "18 juli 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Jan","34,56s"), li(2,"Stefan","35,71s"), li(3,"Ruud","36,12s"), li(4,"Rob","38,02s"),
        li(5,"Dennis","39,03s"), li(6,"Bert","40,48s"), li(7,"Frank M.","40,56s"), li(8,"Koen","40,98s"),
        li(9,"Wouter","41,08s"), li(10,"Ad","45,57s"), li(11,"Dennis W.","45,61s"), li(12,"Bram","47,53s"),
        li(13,"Jorgen","48,89s"), li(14,"Ivan","49,36s"), li(15,"Richard","49,50s"), li(16,"Jeroen","50,21s"),
        li(17,"Aldo","51,14s"), li(18,"Robert","51,15s"), li(19,"Pieter","51,41s"), li(20,"Sjaak","53,61s"),
        li(21,"Robin","53,80s"), li(22,"Niels","53,88s"), li(23,"Roderick","55,28s"), li(24,"Ray","59,47s"),
        li(25,"Frank B.","66,00s"), li(26,"Arjan","67,00s"), li(27,"Udo","96,00s"),
    ]) + cat("Dames") + ul([
        li(1,"Vivian","31,25s"), li(2,"Gaoya","34,50s"), li(3,"Wendy","37,50s"), li(4,"Manon","40,03s"),
        li(5,"Dyonne","40,86s"), li(6,"Cynthia","43,06s"), li(7,"Pascale","43,63s"), li(8,"Fiona","43,80s"),
        li(9,"Janneke","44,00s"), li(10,"Liesbeth","45,78s"), li(11,"Bente","48,72s"), li(12,"Cathy","50,16s"),
        li(13,"Marije","51,12s"), li(14,"Fleur","52,50s"), li(15,"Eef","54,32s"), li(16,"Gloria","55,08s"),
        li(17,"Anne","62,00s"), li(18,"Mirthe","65,00s"), li(19,"Paula","116,00s"),
    ])
)

# ── #80 ───────────────────────────────────────────────────────────────────────
c80 = acc(80, "86,4 meter sprint challenge", "13 juli 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Ivan","11,33s"), li(2,"Robert","11,72s"), li(3,"Ravi","11,94s"), li(4,"Wouter","11,73s"),
        li(5,"Robert v.R.","12,25s"), li(6,"Bart","12,36s"), li(7,"Bram","12,37s"), li(8,"Alex","12,73s"),
        li(9,"Koen","12,87s"), li(10,"Jorgen","13,02s"), li(11,"Max","13,04s"), li(12,"Roderick","13,53s"),
        li(13,"Kampie","13,55s"), li(14,"Ruud","13,63s"), li(15,"Aldo","13,84s"), li(16,"Rob","14,05s"),
        li(17,"Faasie","14,12s"), li(18,"Frank M.","14,31s"), li(19,"Robin","14,61s"), li(20,"Stefan","14,70s"),
        li(21,"Richard","15,61s"), li(22,"Theo","16,39s"), li(23,"Ammesh","16,72s"), li(24,"Frank","17,56s"),
        li(25,"AD","18,10s"), li(26,"Sjaak","18,37s"),
    ]) + cat("Dames") + ul([
        li(1,"Gwen","13,94s"), li(2,"Vivian","13,98s"), li(3,"Gloria","14,08s"), li(4,"Charissa","14,19s"),
        li(5,"Gaoya","14,34s"), li(6,"Manon","14,36s"), li(7,"Wendy","14,42s"), li(8,"Cynthia","15,45s"),
        li(9,"Dyonne","15,76s"), li(10,"Bente","15,84s"), li(11,"Minou","15,87s"), li(12,"Liesbeth","16,31s"),
        li(13,"Anne","16,72s"), li(14,"Cathy","17,54s"), li(15,"Paula","23,00s"),
    ])
)

# ── #79 ───────────────────────────────────────────────────────────────────────
c79 = acc(79, "Push-up challenge (60 seconden)", "3 juli 2024",
    note("Meeste push-ups wint &mdash; dobbelsteen aantikken") +
    cat("Heren") + ul([
        li(1,"Mark","71"), li(2,"Robert E.","66"), li(3,"Ravi","55"), li(4,"Niels K.","54"),
        li(4,"Robert R.","54"), li(6,"Roderick","53"), li(7,"Koen","50"), li(7,"Pieter","50"),
        li(9,"Robin","49"), li(10,"Cas JR.","47"), li(11,"Wouter","46"), li(12,"Rob","45"),
        li(13,"Sil","44"), li(14,"Jorgen","43"), li(15,"Peter","41"), li(15,"Max","41"),
        li(17,"Dennis","39"), li(17,"Richard","39"), li(19,"Sjaak","37"), li(20,"Dennis [2]","33"),
        li(21,"Elwin","31"), li(22,"Bram","30"), li(23,"Richard K.","27"), li(24,"Ad","24"),
        li(24,"Jeroen","24"), li(26,"Bart","22"), li(27,"Frank","21"), li(27,"Ruud","21"),
        li(29,"Frank B.","14"),
    ]) + cat("Dames") + ul([
        li(1,"Liesbeth","41 &#127942;"), li(1,"Gloria","41 &#127942;"), li(3,"Charissa","37"),
        li(3,"Fleur","37"), li(5,"Manon","36"), li(5,"Deborah","36"), li(7,"Gaoya","34"),
        li(8,"Cathy","33"), li(9,"Wendy P.","32"), li(10,"Wendy","31"), li(11,"Paula","30"),
        li(12,"Anne","26"), li(13,"Stefanie","25"), li(13,"Fiona","25"), li(15,"Marije","24"),
        li(15,"Dyonne","24"), li(17,"Bente","23"), li(17,"Alice","23"), li(19,"Eef","22"),
        li(20,"Vivian","19"), li(21,"Janneke","16"),
    ])
)

# ── #78 ───────────────────────────────────────────────────────────────────────
c78 = acc(78, "Ringen hangen challenge", "27 juni 2024",
    note("Langste tijd wint") +
    cat("Heren") + ul([
        li(1,"Bart","146s"), li(2,"Cas","130s"), li(3,"Robert","122s"), li(4,"Robin","121s"),
        li(5,"Wouter","104s"), li(6,"Aldo","101s"), li(7,"Frank M.","99s"), li(8,"Rob","90s"),
        li(9,"Bram","87s"), li(10,"Sjaak","83s"), li(11,"Jorgen","82s"), li(12,"Dennis","75s"),
        li(13,"Dennis [2]","73s"), li(14,"Richard","71s"), li(15,"Arjan","70s"), li(16,"Bas","65s"),
        li(17,"Elwin","61s"), li(18,"Peter","59s"), li(19,"Sil","49s"), li(20,"Amresh","47s"),
        li(21,"Jeroen","37s"), li(22,"Ruud","33s"),
    ]) + cat("Dames") + ul([
        li(1,"Bente","142s"), li(2,"Pascale","131s"), li(3,"Gaoya","116s"), li(4,"Cynthia","104s"),
        li(5,"Britt","101s"), li(5,"Charissa","101s"), li(7,"Manon","85s"), li(8,"Wendy","84s"),
        li(9,"Janneke","78s"), li(10,"Fleur","75s"), li(11,"Paula","74s"), li(12,"Fiona","68s"),
        li(13,"Rosalie","65s"), li(14,"Liesbeth","64s"), li(15,"Cathy","62s"), li(16,"Eef","58s"),
        li(17,"Dyonne","50s"), li(18,"Anne","48s"), li(19,"Marije","29s"),
    ])
)

# ── #77 ───────────────────────────────────────────────────────────────────────
c77_h = ul([
    li(1,"Stefan","17,5 kg"),
    li(2,"Aldo","15 kg"), li(2,"Bart","15 kg"), li(2,"Ben","15 kg"), li(2,"Dennis","15 kg"),
    li(2,"Elwin","15 kg"), li(2,"Frank M.","15 kg"), li(2,"Jeroen","15 kg"), li(2,"Jorgen","15 kg"),
    li(2,"Kampie","15 kg"), li(2,"Kevin","15 kg"), li(2,"Mark","15 kg"), li(2,"Radboud","15 kg"),
    li(2,"Rob","15 kg"), li(2,"Robert","15 kg"), li(2,"Robin","15 kg"), li(2,"Roderick","15 kg"),
    li(2,"Ruud","15 kg"), li(2,"Thijs","15 kg"),
    li(20,"Amresh","10 kg"), li(20,"Arjan","10 kg"), li(20,"Dennis [2]","10 kg"),
    li(20,"Frank","10 kg"), li(20,"Frank [2]","10 kg"), li(20,"Henk","10 kg"),
    li(20,"Ivan","10 kg"), li(20,"Jan Zalando","10 kg"), li(20,"Koen","10 kg"),
    li(20,"Max","10 kg"), li(20,"Peter","10 kg"), li(20,"Pieter","10 kg"),
    li(20,"Richard","10 kg"), li(20,"Sil","10 kg"), li(20,"Sjaak","10 kg"),
])
c77_d = ul([
    li(1,"Alice","10 kg"), li(1,"Charissa","10 kg"), li(1,"Cynthia","10 kg"),
    li(1,"Eef","10 kg"), li(1,"Fiona","10 kg"), li(1,"Janneke","10 kg"),
    li(1,"Marije","10 kg"), li(1,"Marloes","10 kg"), li(1,"Nicolette","10 kg"),
    li(10,"Anne","5 kg"), li(10,"Bente","5 kg"), li(10,"Cathy","5 kg"),
    li(10,"Dyonne","5 kg"), li(10,"Gloria","5 kg"), li(10,"Gwen","5 kg"),
    li(10,"Kirsten","5 kg"), li(10,"Liesbeth","5 kg"), li(10,"Madou","5 kg"),
    li(10,"Minou","5 kg"), li(10,"Paula","5 kg"), li(10,"Stefanie","5 kg"),
    li(10,"Wendy","5 kg"),
])
c77 = acc(77, "Schijf flippen en vangen challenge", "19 juni 2024",
    note("Zwaarste schijf wint &mdash; 180&deg; flip opvangen") +
    cat("Heren") + c77_h + cat("Dames") + c77_d
)

# ── #76 ───────────────────────────────────────────────────────────────────────
c76 = acc(76, "Tribune traplopen challenge (5&times; op en af)", "14 juni 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Wouter","38s"), li(2,"Bart","45s"), li(3,"Ruud","46s"), li(4,"Alex","47s"),
        li(5,"Rob","48s"), li(6,"Koen","49s"), li(7,"Robin","50s"), li(8,"Dennis","51s"),
        li(8,"RO","54s"), li(10,"Arjan","56s"), li(11,"Aldo","56s"), li(12,"Jorgen","57s"),
        li(12,"Frank M.","63s"), li(14,"Stefan","66s"), li(15,"Joeri","66s"),
        li(16,"Dennis [2]","74s"), li(17,"Pim","85s"), li(18,"Frank","89s"),
    ]) + cat("Dames") + ul([
        li(1,"Gwen","48s &#127942;"), li(1,"Manon","48s &#127942;"), li(1,"Dyonne","48s &#127942;"),
        li(4,"Gloria","51s"), li(5,"Cynthia","52s"), li(6,"Pascale","56s"), li(7,"Fiona","62s"),
        li(8,"Wendy","63s"), li(8,"Liesbeth","63s"), li(8,"Charissa","63s"), li(8,"Minou","63s"),
        li(12,"Marije","65s"), li(13,"Bente","66s"), li(14,"Cathy","70s"), li(15,"Britt","72s"),
        li(16,"Anne","74s"), li(17,"Eef","77s"),
    ])
)

# ── #75 ───────────────────────────────────────────────────────────────────────
c75 = acc(75, "Farmer&#39;s Walk challenge (4 rondjes)", "6 juni 2024",
    note("Snelste tijd wint (laagste = beter) &mdash; Heren 2&times;24 KG &bull; Dames 2&times;16 KG") +
    cat("Heren") + ul([
        li(1,"Robert","97s"), li(2,"Rob","99s"), li(3,"Jorgen","108s"), li(4,"Ruud","111s"),
        li(5,"Bart","114s"), li(6,"Robin","115s"), li(7,"Aldo","122s"), li(8,"Sjaak","128s"),
        li(8,"Theo","128s"), li(10,"Dennis","129s"), li(11,"Elwin","139s"), li(12,"Koen","143s"),
        li(13,"Roderick","146s"), li(14,"Pieter","171s"), li(15,"Frank Z.","173s"),
        li(16,"Ren&eacute;","191s"), li(17,"Frank B.","239s"),
    ]) + cat("Dames") + ul([
        li(1,"Manon","99s"), li(2,"Dyonne","102s"), li(3,"Cynthia","104s"), li(4,"Vivian","116s"),
        li(5,"Marije","117s"), li(5,"Wendy","117s"), li(7,"Cathy","131s"), li(8,"Wendy P.","138s"),
        li(9,"Alice","145s"), li(10,"Janneke","150s"), li(11,"Monica","152s"), li(12,"Liesbeth","155s"),
    ])
)

# ── #74 ───────────────────────────────────────────────────────────────────────
c74 = acc(74, "120 meter hinkelen challenge", "31 mei 2024",
    note("Snelste tijd wint &mdash; 60m links + 60m rechts") +
    cat("Heren") + ul([
        li(1,"Rob","48s"), li(2,"Ruud","50s"), li(3,"Koen","54s"), li(4,"Dennis","63s"),
        li(5,"Robin","66s"), li(6,"Arjan","69s"), li(7,"Stefan","70s"), li(8,"Aldo","71s"),
        li(9,"Richard","86s"),
    ]) + cat("Dames") + ul([
        li(1,"Gwen","52s"), li(2,"Manon","54s"), li(3,"Pascale","60s"), li(4,"Cynthia","61s"),
        li(5,"Dyonne","64s"), li(6,"Marije","72s"), li(7,"Fiona","82s"),
    ])
)

# ── #73 ───────────────────────────────────────────────────────────────────────
c73 = acc(73, "Battle ropes challenge (100 slagen)", "23 mei 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Radboud","35s"), li(2,"Jorgen","46s"), li(3,"Aldo","51s"), li(4,"Jan","52s"),
        li(5,"Rob","56s"), li(5,"Frank M.","56s"), li(7,"Max","57s"), li(8,"Elwin","57s"),
        li(9,"Stefan","64s"), li(10,"Roderick","68s"), li(11,"Dennis","71s"), li(11,"Peter","71s"),
        li(13,"Ad","78s"), li(14,"Robin","85s"), li(15,"Jeroen","89s"),
    ]) + cat("Dames") + ul([
        li(1,"Wendy P.","37s"), li(2,"Cynthia","39s"), li(3,"Charissa","47s"), li(3,"Cathy","47s"),
        li(5,"Wendy","48s"), li(6,"Bente","50s"), li(6,"Anne","50s"), li(8,"Gloria","52s"),
        li(9,"Fiona","55s"), li(10,"Vivianne","62s"), li(11,"Marije","68s"), li(12,"Paula","96s"),
    ])
)

# ── #72 ───────────────────────────────────────────────────────────────────────
c72 = acc(72, "Sentadilla espa&ntilde;ola challenge (Spanish squat)", "18 mei 2024",
    note("Langste tijd wint &mdash; elastiek, op &eacute;&eacute;n been") +
    cat("Heren") + ul([
        li(1,"Kevin Z","150s"), li(2,"Robin","134s"), li(3,"Koen","104s"), li(4,"Aldo","93s"),
        li(5,"Niels E.","91s"), li(6,"Jorgen","85s"), li(7,"Bjorn","82s"), li(8,"John","70s"),
        li(9,"Ruud","69s"), li(10,"Sjaak","65s"), li(11,"Sil","62s"), li(12,"Ad","60s"),
        li(12,"Sven","60s"), li(14,"Frank","56s"), li(14,"Pieter","56s"), li(16,"Roderick","54s"),
        li(17,"Stefan","46s"), li(18,"Dennis","43s"), li(19,"Frank B.","41s"), li(20,"Bram","40s"),
        li(21,"Udo","33s"), li(22,"Amresh","27s"),
    ]) + cat("Dames") + ul([
        li(1,"Pascale","150s"), li(2,"Monica","140s"), li(3,"Paula","125s"), li(4,"Minou","95s"),
        li(5,"Cynthia","100s"), li(6,"Cathy","80s"), li(7,"Fiona","68s"), li(8,"Kirsten","48s"),
        li(9,"Britt","46s"), li(10,"Alice","45s"), li(11,"Vivianne","42s"),
    ])
)

# ── #71 ───────────────────────────────────────────────────────────────────────
c71 = acc(71, "Kettlebell chin-up challenge (2 minuten)", "2 mei 2024",
    note("Meeste herhalingen wint &mdash; Dames: 16 KG kettlebell") +
    cat("Heren") + ul([
        li(1,"Frank M.","76"), li(2,"Jorgen","71"), li(3,"Aldo","63"), li(4,"Sjaak","61"),
        li(5,"Ad","55"), li(6,"Stefan","54"), li(7,"Dennis","52"), li(8,"Frank","42"),
    ]) + cat("Dames (16 KG)") + ul([
        li(1,"Gaoya","90"), li(2,"Manon","85"), li(3,"Pascalle","74"), li(4,"Dyonne","72"),
        li(5,"Liesbeth","61"), li(6,"Cynthia","52"), li(7,"Paula","45"),
    ])
)

# ── #70 ───────────────────────────────────────────────────────────────────────
c70 = acc(70, "Leg press challenge (10 RM)", "24 april 2024",
    note("Zwaarste gewicht wint &times;10 herhalingen") +
    cat("Heren") + ul([
        li(1,"Stefan","200 kg"), li(1,"Ravi","200 kg"), li(3,"Kevin VdL","190 kg"),
        li(4,"Jorgen","180 kg"), li(4,"Frank M","180 kg"), li(6,"Dennis","170 kg"),
        li(6,"Radboud","170 kg"), li(8,"Ruud","160 kg"), li(8,"Robert E.","160 kg"),
        li(8,"Sjaak","160 kg"), li(8,"Elwin","160 kg"), li(12,"Jan","150 kg"),
        li(12,"Robert E. [2]","150 kg"), li(12,"Jeroen","150 kg"), li(15,"Kampie","140 kg"),
        li(15,"Robert v R","140 kg"), li(15,"Wout","140 kg"), li(18,"Koen","130 kg"),
        li(19,"Frank","120 kg"), li(19,"Aldo","120 kg"), li(19,"Pieter","120 kg"),
        li(22,"Ad","110 kg"), li(22,"Theo","110 kg"), li(24,"Richard","100 kg"),
        li(25,"Ray","90 kg"), li(26,"Frank [2]","80 kg"),
    ]) + cat("Dames") + ul([
        li(1,"Gaoya","150 kg"), li(2,"Wendy","140 kg"), li(3,"Minou","130 kg"),
        li(4,"Cathy","110 kg"), li(4,"Gloria","110 kg"), li(6,"Manon","100 kg"),
        li(6,"Liesbeth","100 kg"), li(6,"Charissa","100 kg"), li(6,"Anne","100 kg"),
        li(10,"Gwen","90 kg"), li(10,"Dyonne","90 kg"), li(10,"Nienke","90 kg"),
        li(10,"Stefanie","90 kg"), li(14,"Paula","80 kg"), li(14,"Cynthia","80 kg"),
        li(14,"Alice","80 kg"),
    ])
)

# ── #69 ───────────────────────────────────────────────────────────────────────
c69 = acc(69, "Dumbbell press challenge (8 KG)", "18 april 2024",
    note("Meeste herhalingen wint") +
    cat("Heren") + ul([
        li(1,"Mark","60"), li(2,"Robert v R.","49"), li(3,"Stefan","45"), li(4,"Rob","42"),
        li(5,"Jorgen","41"), li(6,"Robert E.","40"), li(7,"Pieter","36"), li(7,"Wouter","36"),
        li(9,"Ad","35"), li(9,"Jan","35"), li(9,"Ren&eacute;","35"), li(12,"Roderick","33"),
        li(13,"Kevin Z","29"), li(14,"Dennis","27"), li(15,"Aldo","24"), li(15,"Sjaak","24"),
        li(17,"Jeroen","23"), li(18,"Koen","22"), li(19,"Chico","21"), li(20,"Frank","19"),
        li(21,"Richard","14"),
    ]) + cat("Dames") + ul([
        li(1,"Cathy","120"), li(2,"Marije","105"), li(3,"Gaoya","100"), li(4,"Liesbeth","71"),
        li(5,"Bente","70"), li(6,"Stefanie","65"), li(7,"Manon","64"), li(8,"Cynthia","60"),
        li(9,"Minou","50"), li(9,"Janneke","50"), li(9,"Charissa","50"), li(12,"Gloria","45"),
        li(13,"Dyonne","44"), li(14,"Pascale","35"), li(15,"Paula","27"), li(16,"Bjornelien","16"),
    ])
)

# ── #68 ───────────────────────────────────────────────────────────────────────
c68 = acc(68, "Bench press challenge (120 seconden)", "5 april 2024",
    note("Meeste herhalingen wint") +
    cat("Heren") + ul([
        li(1,"Roderick","120"), li(2,"Kevin Z","116"), li(3,"Bert","114"), li(4,"Stefan","105"),
        li(4,"Robert","105"), li(6,"Radboud","103"), li(7,"Dennis","101"), li(8,"Rene","92"),
        li(9,"Pieter","91"), li(10,"Jorgen","90"), li(10,"Jan","90"), li(12,"Paul","88"),
        li(12,"Frank M","88"), li(14,"Alex","85"), li(15,"Jeroen","80"), li(16,"Richard","65"),
        li(17,"Peter","64"), li(18,"Koen","63"), li(19,"Max","60"), li(19,"Ad","60"),
        li(21,"Aldo","59"), li(22,"Ivan","49"), li(23,"Deen","43"), li(24,"Frank O","42"),
    ]) + cat("Dames") + ul([
        li(1,"Stefanie","106"), li(2,"Cathy","104"), li(3,"Marije","90"), li(4,"Gaoya","88"),
        li(5,"Mirthe","80"), li(5,"Liesbeth","80"), li(7,"Fiona","75"), li(8,"Bente","74"),
        li(9,"Manon","71"), li(10,"Dyonne","70"), li(11,"Minou","69"), li(12,"Nienke","64"),
        li(13,"Petra","62"), li(14,"Cynthia","52"), li(15,"Paula","50"), li(16,"Britt","44"),
    ])
)

# ── #67 ───────────────────────────────────────────────────────────────────────
c67 = acc(67, "Box jump challenge (180 seconden)", "27 maart 2024",
    note("Meeste sprongen wint") +
    cat("Heren") + ul([
        li(1,"Mark K.","105"), li(2,"Jorgen","69"), li(3,"Pim","62"),
        li(4,"Dennis","53"), li(5,"Ad","49"), li(6,"Sil","36"),
    ]) + cat("Dames") + ul([
        li(1,"Gwen","84"), li(2,"Gaoya","77"), li(3,"Manon","72"), li(4,"Lindy","68"),
        li(5,"Paula","61"), li(5,"Marije","61"), li(7,"Cathy","60"), li(8,"Fiona","59"),
        li(9,"Lotte","54"),
    ])
)

# ── #66 ───────────────────────────────────────────────────────────────────────
c66 = acc(66, "Windmill challenge (50 windmills)", "22 maart 2024",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Roderick","0:52"), li(2,"Jorgen","0:53"), li(3,"Jan","0:57"), li(4,"Ruud","1:01"),
        li(5,"Dennis","1:03"), li(5,"Peter","1:03"), li(7,"Pieter","1:05"), li(8,"Faasie","1:07"),
        li(9,"Sjaak","1:08"), li(10,"Ad","1:19"), li(11,"Rene","1:23"), li(12,"Rob","1:31"),
        li(13,"Aldo","1:33"), li(14,"Paul","1:50"), li(15,"Chico","1:51"), li(16,"Jeroen","2:02"),
        li(17,"Rene [2]","2:12"), li(18,"Amresh","2:24"), li(19,"Richard","3:39"),
    ]) + cat("Dames") + ul([
        li(1,"Cathy","0:45"), li(2,"Gaoya","0:46"), li(3,"Dyonne","0:47"), li(4,"Manon","0:48"),
        li(5,"Liesbeth","0:50"), li(6,"Marije","0:52"), li(7,"Wendy","0:53"), li(8,"Bente","1:04"),
        li(8,"Janneke","1:04"), li(10,"Paula","1:05"), li(11,"Pascale","1:09"), li(12,"Fiona","1:16"),
        li(13,"Stefanie","1:17"), li(13,"Petra","1:17"), li(15,"Nienke","1:25"),
    ])
)

# ── #65 ───────────────────────────────────────────────────────────────────────
c65 = acc(65, "Dumbbell Dash challenge", "14 maart 2024",
    note("Snelste tijd wint &mdash; heen en weer op handen en voeten, dumbbells aantikken") +
    cat("Heren") + ul([
        li(1,"Sil","28,17s"), li(2,"Radboud","30,80s"), li(3,"Roderick","32,23s"),
        li(4,"Tygo","33,29s"), li(5,"Ruud","34,50s"), li(6,"Ravi","35,34s"),
        li(7,"Jorgen","37,92s"), li(8,"Max","39,33s"), li(9,"Faasie","40,44s"),
        li(10,"Rob","41,50s"), li(11,"Frank","46,79s"), li(12,"Ren&eacute;","47,15s"),
        li(13,"Theo","47,20s"), li(14,"Frank B.","48,09s"), li(15,"Peter","49,01s"),
        li(16,"Kees","50,05s"), li(17,"Dennis","54,44s"), li(18,"Sjaak","56,67s"),
        li(19,"Richard","59,00s"),
    ]) + cat("Dames") + ul([
        li(1,"Dyonne","38,30s"), li(2,"Wendy","38,80s"), li(3,"Manon","39,35s"),
        li(4,"Gloria","39,66s"), li(5,"Cathy","40,96s"), li(6,"Gaoya","42,68s"),
        li(7,"Liesbeth","47,09s"), li(8,"Pascale","48,70s"), li(9,"Charissa","54,39s"),
        li(10,"Marije","55,30s"), li(11,"Paula","67,01s"), li(12,"Nienke","67,30s"),
        li(13,"Kirsten","68,60s"), li(14,"Britt","72,39s"),
    ])
)

# ── #64 ───────────────────────────────────────────────────────────────────────
c64 = acc(64, "Trapbar Flamingo Showdown", "9 maart 2024",
    note("Zwaarste gewicht wint &mdash; op 1 been, gewicht omhoog schuiven") +
    cat("Heren") + ul([
        li(1,"Ruud","30 kg"), li(2,"Radboud","25 kg"), li(2,"Kees","25 kg"),
        li(4,"Mark","20 kg"), li(4,"Jorgen","20 kg"), li(4,"Kevin Val","20 kg"),
        li(4,"Robert","20 kg"), li(4,"Ren&eacute;","20 kg"), li(9,"Kevin Z","15 kg"),
        li(9,"Rob","15 kg"), li(9,"Bas","15 kg"), li(9,"Frank M.","15 kg"),
        li(9,"Elwin","15 kg"), li(14,"Ravi","10 kg"), li(14,"Roderick","10 kg"),
        li(14,"Stefan","10 kg"), li(14,"Sjaak","10 kg"), li(14,"Jeroen","10 kg"),
        li(14,"Peter","10 kg"), li(14,"Amresh","10 kg"), li(14,"Theo","10 kg"),
        li(22,"Niels","7,5 kg"), li(23,"Frank B","5 kg"), li(23,"Robert Zalando","5 kg"),
        li(23,"Dennis","5 kg"), li(23,"Sil","5 kg"), li(27,"Richard","2,5 kg"),
    ]) + cat("Dames") + ul([
        li(1,"Bente","20 kg"), li(2,"Manon","15 kg"), li(3,"Nicolette","10 kg"),
        li(3,"Minou","10 kg"), li(3,"Gaoya","10 kg"), li(3,"Dyonne","10 kg"),
        li(3,"Liesbeth","10 kg"), li(3,"Monica","10 kg"), li(9,"Madou","7,5 kg"),
        li(10,"Paula","5 kg"), li(10,"Cathy","5 kg"), li(10,"Janneke","5 kg"),
        li(10,"Wendy","5 kg"), li(10,"Pascale","5 kg"), li(10,"Nienke","5 kg"),
        li(10,"Stefanie","5 kg"), li(10,"Britt","5 kg"), li(10,"Kirsten","5 kg"),
        li(10,"Fiona","5 kg"),
    ])
)

# ── #63 ───────────────────────────────────────────────────────────────────────
c63 = acc(63, "10 RM Trapbar Deadlift", "28 februari 2024",
    note("Zwaarste gewicht wint &times;10 herhalingen") +
    cat("Heren") + ul([
        li(1,"Ravi","140 kg"), li(2,"Ruud","130 kg"), li(2,"Jan","130 kg"),
        li(4,"Roderick","120 kg"), li(4,"Elwin","120 kg"), li(6,"Wouter","100 kg"),
        li(6,"Kees","100 kg"), li(8,"Frank","90 kg"), li(8,"Rob","90 kg"),
        li(8,"Sjaak","90 kg"), li(11,"Amresh","70 kg"), li(12,"Faas","60 kg"),
    ]) + cat("Dames") + ul([
        li(1,"Wendy","110 kg"), li(2,"Gaoya","100 kg"), li(3,"Marije","90 kg"),
        li(4,"Cathy","85 kg"), li(5,"Bente","80 kg"), li(6,"Paula","60 kg"),
        li(6,"Nienke","60 kg"), li(6,"Stefanie","60 kg"), li(9,"Britt","55 kg"),
        li(9,"Fiona","55 kg"),
    ])
)

# ── #62 ───────────────────────────────────────────────────────────────────────
c62 = acc(62, "Leg raises challenge (hangend, max herhalingen)", "22 februari 2024",
    note("Meeste herhalingen wint") +
    cat("Heren") + ul([
        li(1,"Ben","50"), li(2,"Robert","40"), li(2,"Rene","40"), li(4,"Bas","38"),
        li(5,"Kees","36"), li(6,"Rene [2]","33"), li(7,"Sjaak","28"), li(8,"Theo","26"),
        li(9,"Rowdy","25"), li(9,"Peter","25"), li(9,"Wouter","25"), li(12,"Stefan","24"),
        li(12,"Kevin Z","24"), li(14,"Ruud","23"), li(15,"Roderick","22"), li(16,"Jan","21"),
        li(17,"Frank B","20"), li(18,"Rob","18"), li(19,"Dennis","17"), li(20,"Ad","16"),
        li(21,"Richard","15"), li(21,"Pieter","15"), li(23,"Jorgen","14"),
    ]) + cat("Dames") + ul([
        li(1,"Manon","40"), li(2,"Wendy","32"), li(3,"Gloria","31"), li(4,"Nicolette","26"),
        li(5,"Cathy","25"), li(5,"Liesbeth","25"), li(7,"Dyonne","23"), li(8,"Marije","20"),
        li(8,"Charissa","20"), li(10,"Paula","13"), li(10,"Gaoya","13"), li(10,"Fiona","13"),
        li(13,"Monica","11"), li(14,"Britt","9"),
    ])
)

# ── #61 ───────────────────────────────────────────────────────────────────────
c61 = acc(61, "Bosu balance challenge (1 been + voetbal)", "17 februari 2024",
    note("Langste tijd wint") +
    cat("Heren") + ul([
        li(1,"Sil","270s"), li(2,"Kevin Z.","148s"), li(3,"Bink","145s"), li(4,"Mark","91s"),
        li(5,"Mark K.","71s"), li(6,"Frenkie","65s"), li(7,"Ravi","59s"), li(8,"Stefan","55s"),
        li(9,"Tygo","40s"), li(10,"Jan","36s"), li(10,"Rob","36s"), li(12,"Jorgen","32s"),
        li(13,"Robert","29s"), li(14,"Roderick","28s"), li(15,"Ruud","25s"), li(15,"Richard","25s"),
        li(17,"Niels","24s"), li(18,"Dennis","20s"), li(19,"Elwin","13s"), li(20,"Amresh","12s"),
        li(21,"Peter","11s"), li(22,"Ad","8s"), li(22,"Sjaak","8s"), li(24,"Jeroen","7s"),
        li(25,"Frank B.","4s"), li(25,"Frank M.","4s"),
    ]) + cat("Dames") + ul([
        li(1,"Charissa","85s"), li(2,"Kirsten","74s"), li(2,"Wendy","74s"), li(4,"Fiona","73s"),
        li(5,"Gloria","70s"), li(6,"Bente","66s"), li(7,"Cathy","33s"), li(7,"Minou","33s"),
        li(9,"Gaoya","31s"), li(10,"Gwen","25s"), li(11,"Marije","24s"), li(12,"Nicolet","23s"),
        li(13,"Madou","20s"), li(14,"Dyonne","17s"), li(15,"Liesbeth","16s"), li(16,"Manon","15s"),
        li(16,"Anne","15s"), li(16,"Nienke","15s"), li(19,"Stefanie","7s"), li(20,"Paula","6s"),
        li(21,"Zare","5s"), li(21,"Janneke","5s"),
    ])
)

# ── #60 ───────────────────────────────────────────────────────────────────────
c60 = acc(60, "Assisted pull-up challenge (max herhalingen)", "31 januari 2024",
    note("Meeste herhalingen wint") +
    cat("Heren") + ul([
        li(1,"Ben","40x"), li(2,"Mark","34x"), li(3,"Sepp","33x"), li(4,"Sil","30x"),
        li(5,"Radboud","29x"), li(6,"Ravi","26x"), li(7,"Kees","24x"), li(8,"Jorgen","23x"),
        li(8,"Cas Junior","23x"), li(10,"Aldo","22x"), li(11,"Jan","18x"), li(12,"Wouter","13x"),
        li(13,"Roderick","12x"), li(13,"Ruud","12x"), li(15,"Ad","10x"), li(16,"Pieter","9x"),
        li(17,"Richard","8x"), li(18,"Dennis","7x"), li(18,"Frank","7x"),
    ]) + cat("Dames") + ul([
        li(1,"Cathy","25x"), li(2,"Charissa","24x"), li(3,"Bente","22x"), li(4,"Cynthia","20x"),
        li(5,"Paula","17x"), li(6,"Wendy P.","14x"), li(7,"Britt","6x"), li(8,"Marije","5x"),
        li(8,"Gaoya","5x"),
    ])
)

# ── #59 ───────────────────────────────────────────────────────────────────────
c59 = acc(59, "3 minuten roeien challenge", "25 januari 2024",
    note("Langste afstand wint (meters in 3 minuten)") +
    cat("Heren") + ul([
        li(1,"Kevin","918 m"), li(2,"Rob","889 m"), li(3,"Ruud","879 m"), li(4,"Mark","878 m"),
        li(5,"Jeroen","846 m"), li(6,"Aldo","840 m"), li(7,"Robert","838 m"), li(8,"Wouter","829 m"),
        li(9,"Elwin","822 m"), li(10,"Roderick","817 m"), li(11,"Sjaak","811 m"), li(12,"Theo","789 m"),
        li(13,"Peter","788 m"), li(14,"Jorgen","786 m"), li(15,"Kees","775 m"), li(16,"Dennis","772 m"),
        li(17,"Stefan","767 m"), li(18,"Faasie","764 m"), li(19,"Frank","693 m"),
    ]) + cat("Dames") + ul([
        li(1,"Wendy P.","799 m"), li(2,"Cynthia","788 m"), li(3,"Marije","771 m"), li(4,"Minou","769 m"),
        li(5,"Stefanie","765 m"), li(6,"Cathy","759 m"), li(7,"Bente","750 m"), li(8,"Manon","730 m"),
        li(9,"Nienke","724 m"), li(10,"Dyonne","711 m"), li(11,"Liesbeth","696 m"), li(12,"Madou","693 m"),
        li(13,"Janneke","686 m"), li(14,"Fiona","683 m"), li(15,"Paula","674 m"), li(16,"Gwen","670 m"),
        li(17,"Kirsten","659 m"), li(18,"Marieke","632 m"), li(19,"Britt","575 m"),
    ])
)

# ── #58 ───────────────────────────────────────────────────────────────────────
c58 = acc(58, "Nieuwjaarschallenge 2024", "20 januari 2024",
    note("Snelste tijd wint &mdash; 24 squats + 24 lunges + 24 sit-ups + 24 push-ups + 24 boxdips + 24 bicep curls") +
    cat("Heren") + ul([
        li(1,"Thijs","3:34"), li(2,"Bas","3:35"), li(3,"Aldo","3:41"), li(4,"Kevin","3:52"),
        li(5,"Sjaak","4:29"), li(6,"Jorgen","4:33"), li(7,"Kees","4:46"), li(8,"Richard","8:44"),
    ]) + cat("Dames") + ul([
        li(1,"Manon","3:02"), li(2,"Cathy","3:06"), li(3,"Marije","3:10"), li(4,"Gaoya","3:15"),
        li(5,"Mirthe","3:24"), li(6,"Charissa","3:38"), li(6,"Gloria","3:38"), li(6,"Dyonne","3:38"),
        li(9,"Bente","3:39"), li(10,"Cynthia","4:02"), li(11,"Anne","4:03"), li(12,"Fiona","4:13"),
        li(13,"Liesbeth","4:17"), li(14,"Britt","5:06"), li(15,"Nienke","6:18"), li(16,"Stefanie","6:26"),
    ])
)

# ── #57 ───────────────────────────────────────────────────────────────────────
c57 = acc(57, "TRX Row challenge (max herhalingen)", "10 januari 2024",
    note("Meeste herhalingen wint") +
    cat("Heren") + ul([
        li(1,"Robert","63x"), li(2,"Bert","60x"), li(3,"Sepp","58x"), li(4,"Niels K.","54x"),
        li(5,"Peter","53x"), li(5,"Radboud","53x"), li(7,"Rene","52x"), li(8,"Ivan","51x"),
        li(8,"Jorgen","51x"), li(10,"Kees","47x"), li(11,"Roderick","43x"), li(12,"Ad","40x"),
        li(13,"Theo","37x"), li(14,"Richard","36x"), li(15,"Rob","35x"), li(16,"Mark","34x"),
        li(17,"Dennis","33x"), li(17,"Stefan","33x"), li(19,"Sjaak","32x"), li(20,"Pieter","31x"),
        li(21,"Frank B.","30x"), li(21,"Elwin","30x"), li(21,"Aldo","30x"),
        li(24,"Jeroen","27x"), li(24,"Niels E.","27x"),
    ]) + cat("Dames") + ul([
        li(1,"Bente","51x"), li(2,"Liesbeth","43x"), li(3,"Manon","39x"), li(4,"Cathy","37x"),
        li(5,"Lotte","34x"), li(6,"Cynthia","33x"), li(7,"Paula","33x"), li(8,"Gaoya","32x"),
        li(9,"Britt","31x"), li(10,"Marije","31x"), li(11,"Nienke","25x"), li(12,"Dyonne","22x"),
        li(13,"Esther","20x"), li(14,"Stefanie","16x"), li(15,"Yvonne","15x"),
        li(16,"Madou","15x"), li(17,"Petra","12x"), li(18,"Kirsten","12x"),
    ])
)

# ── #56 ───────────────────────────────────────────────────────────────────────
c56 = acc(56, "Walking lunges challenge (zo ver mogelijk)", "8 januari 2024",
    note("Langste afstand wint") +
    cat("Heren (2&times;10 KG)") + ul([
        li(1,"Frank M.","80m"), li(2,"Rene","70m"), li(3,"Kevin","66m"), li(4,"Aldo","50m"),
        li(5,"Dennis","42m"), li(6,"Sjaak","38m"), li(7,"Jeroen","37m"), li(8,"Richard","34m"),
    ]) + cat("Dames (2&times;5 KG)") + ul([
        li(1,"Minou","66m"), li(2,"Lotte","64m"), li(3,"Cynthia","63m"), li(4,"Cathy","62m"),
        li(5,"Gloria","59m"), li(6,"Bente","55m"), li(7,"Anne","40m"), li(7,"Fiona","40m"),
        li(9,"Esther","29m"), li(10,"Nienke","27m"),
    ]) + cat("Genderneutraal (zonder gewicht)") + ul([
        li(1,"Niels","60m"), li(2,"Kees","57m"), li(3,"Sanne","54m"), li(4,"Britt","53m"),
        li(5,"Kirsten","49m"), li(6,"Madou","48m"), li(7,"Petra","40m"), li(8,"Stefanie","35m"),
    ])
)

# ── #55 ───────────────────────────────────────────────────────────────────────
c55 = acc(55, "Shoulder Press challenge (max herhalingen)", "7 januari 2024",
    note("Meeste herhalingen wint") +
    cat("Heren") + ul([
        li(1,"Radboud","86x"), li(2,"Mark","73x"), li(3,"Ben","67x"), li(4,"Thijs","57x"),
        li(5,"Elwin","56x"), li(6,"Frank M.","54x"), li(7,"Dennis","52x"), li(8,"Pieter","51x"),
        li(9,"Rob","48x"), li(10,"Sepp","46x"), li(11,"Rene","45x"), li(12,"Jorgen","42x"),
        li(13,"Stijn","39x"), li(14,"Aldo","37x"), li(15,"Jeroen","36x"), li(16,"Roderick","35x"),
        li(17,"Kees","32x"), li(17,"Sjaak","32x"), li(19,"Richard","31x"), li(19,"Bink","31x"),
        li(21,"Kian","30x"),
    ]) + cat("Dames") + ul([
        li(1,"Cathy","78x"), li(2,"Wendy P.","77x"), li(3,"Fiona","72x"), li(4,"Marije","71x"),
        li(5,"Liesbeth","66x"), li(6,"Bente","62x"), li(6,"Manon","62x"), li(8,"Dyonne","60x"),
        li(9,"Mirthe","55x"), li(10,"Lotte","54x"), li(11,"Esther","44x"), li(12,"Paula","43x"),
        li(13,"Nienke","41x"), li(14,"Stefanie","37x"), li(15,"Petra","30x"),
    ])
)

# ── Assemble #87 → #55 ───────────────────────────────────────────────────────
new_challenges = "".join([
    c87,c86,c85,c84,c83,c82,c81,c80,c79,c78,c77,c76,c75,c74,c73,c72,
    c71,c70,c69,c68,c67,c66,c65,c64,c63,c62,c61,c60,c59,c58,c57,c56,c55,"\n"
])

# ── Updated stats ─────────────────────────────────────────────────────────────
NEW_STATS = """  <div class="ff-stats-grid">

    <div class="ff-stat-card">
      <h3>&#127942; Meest gewonnen (1e plaats)</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Gwen</span><span class="stat-val">13&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Radboud</span><span class="stat-val">11&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Gaoya</span><span class="stat-val">11&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Manon</span><span class="stat-val">9&times; gewonnen</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128100; Meest deelgenomen</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Dennis</span><span class="stat-val">79 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Sjaak</span><span class="stat-val">75 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Stefan</span><span class="stat-val">65 challenges</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128293; Records per challenge</h3>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Paalhang</span><span class="stat-val">Jennifer &bull; 257s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Wallsit</span><span class="stat-val">Gaoya &bull; 490s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Wall Sit (2024)</span><span class="stat-val">Gwen &bull; 426s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">500m Roeien</span><span class="stat-val">Kevin &bull; 1:33</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Roeien 3 min</span><span class="stat-val">Kevin &bull; 918m</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Pull Ups</span><span class="stat-val">Monique &bull; 48x</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Shoulder Taps</span><span class="stat-val">Jorgen &bull; 340 (2022)</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Deadhang</span><span class="stat-val">Kees &bull; 2:43</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Bench Press 1RM</span><span class="stat-val">Radboud &bull; 97,5 KG</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Lat Pulldown 1RM</span><span class="stat-val">Robert &bull; 71 KG</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Leg Press 10RM</span><span class="stat-val">Stefan / Ravi &bull; 200 KG</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Assault bike watt</span><span class="stat-val">Stefan &bull; 1278W</span></div>
    </div>

  </div>"""

# ── Fetch & patch ─────────────────────────────────────────────────────────────
print("Ophalen pagina…")
r = requests.get(f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit", auth=auth)
r.raise_for_status()
content = r.json()["content"]["raw"]

INSERTION = "<!-- 54: 5"
matches = [(i, content[i:i+40]) for i in range(len(content)) if content[i:].startswith("<!-- 54:")]
print(f"Insertion marker found at: {matches[0][0] if matches else 'NOT FOUND'}")
if not matches:
    print("FOUT: marker niet gevonden!"); exit(1)

insertion_point = content.find("<!-- 54:")
updated = content[:insertion_point] + new_challenges + "    " + content[insertion_point:]

# Replace stats
start = updated.rfind('<div class="ff-stats-grid">')
end   = updated.find('<div class="ff-updated"', start)
updated = updated[:start] + NEW_STATS + "\n\n  " + updated[end:]

print("Bijwerken pagina…")
r2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}",
    auth=auth,
    json={"content": updated, "status": "draft"}
)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    print(f"✓ Klaar! Preview: https://funfit.nu/?page_id={PAGE_ID}")
else:
    print("Fout:", r2.text[:400])
