#!/usr/bin/env python3
"""Voegt challenges #41–54 toe aan de WordPress leaderboard pagina."""
import requests

WP_URL  = "https://funfit.nu"
auth    = ("info@funfit.nu", "he5r rquj NMuD hXOU KSU2 5rZa")
PAGE_ID = 5477

# ── Helpers ──────────────────────────────────────────────────────────────────
def li(rank, name, score):
    return (f'<li><span class="acc-rank">{rank}</span>'
            f'<span class="acc-name">{name}</span>'
            f'<span class="acc-score">{score}</span></li>')

def ul(items):
    return '<ul class="ff-acc-list">' + "".join(items) + "</ul>"

def cat(label):
    return f'<p style="font-size:.85rem;font-weight:700;margin:14px 0 4px">{label}</p>'

def note(text):
    return f'<p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">{text}</p>'

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
      <div class="ff-acc-body">
        <div class="ff-acc-inner">
          {inner}
        </div>
      </div>
    </div>"""

# ── Challenge #54 ─────────────────────────────────────────────────────────────
c54 = acc(54, "5&times; kunstgrasmat sprint heen en weer", "21 december 2023",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Joey","24,89s"), li(2,"Ravi","25,18s"), li(3,"Ivan","25,20s"),
        li(4,"Bink","25,64s"), li(5,"Tygo","26,10s"), li(6,"Kevin","26,49s"),
        li(7,"Mark","26,80s"), li(8,"Jan","26,82s"), li(9,"Radboud","26,86s"),
        li(10,"Ruud","27,06s"), li(11,"Sepp","27,16s"), li(12,"Robert","27,62s"),
        li(13,"Roderick","27,63s"), li(14,"Kian","27,64s"), li(15,"Robert [2]","27,66s"),
        li(16,"Kampie","28,14s"), li(17,"Sil","28,80s"), li(18,"JW","28,96s"),
        li(18,"Jorgen","28,96s"), li(20,"Rene","30,77s"), li(21,"Faas","30,90s"),
        li(22,"Aldo","32,01s"), li(23,"Sjaak","33,73s"), li(24,"Cas","34,29s"),
        li(25,"Ad","36,07s"), li(26,"Amresh","36,38s"), li(27,"Frank B.","37,04s"),
    ]) +
    cat("Dames") + ul([
        li(1,"Gwen","27,00s"), li(2,"Lotte","27,86s"), li(3,"Manon","29,55s"),
        li(4,"Dyonne","30,10s"), li(5,"Liesbeth","30,60s"), li(6,"Deborah","31,01s"),
        li(7,"Bente","31,30s"), li(8,"Cathy","32,20s"), li(9,"Britt","32,83s"),
        li(10,"Marije","33,40s"), li(11,"Dieuwertje","34,23s"), li(12,"Fiona","35,49s"),
        li(13,"Paula","38,60s"),
    ])
)

# ── Challenge #53 ─────────────────────────────────────────────────────────────
c53 = acc(53, "Lat Pulldown Challenge (1 rep max)", "7 december 2023",
    note("Zwaarste gewicht wint") +
    cat("Heren") + ul([
        li(1,"Robert","71 kg"), li(2,"Jorgen","70,5 kg"), li(3,"Rob","70 kg"),
        li(4,"Radboud","68 kg"), li(5,"Ruud","65 kg"), li(6,"Stefan","62 kg"),
        li(7,"Dennis","60 kg"), li(7,"Frank M.","60 kg"), li(7,"Kees","60 kg"),
        li(10,"Peter","55 kg"), li(10,"Elwin","55 kg"), li(13,"Ad","50 kg"),
        li(13,"Roderick","50 kg"), li(13,"Bink","50 kg"), li(13,"Frankly","50 kg"),
        li(13,"Niels","50 kg"), li(17,"Frank","45 kg"), li(17,"Sil","45 kg"),
        li(17,"Richard","45 kg"), li(17,"Ravi","45 kg"), li(21,"Frank [2]","30 kg"),
    ]) +
    cat("Dames") + ul([
        li(1,"Wendy P.","50 kg"), li(2,"Wendy","46 kg"), li(3,"Bente","45 kg"),
        li(3,"Marije","45 kg"), li(3,"Minou","45 kg"), li(6,"Cathy","40 kg"),
        li(6,"Stefanie","40 kg"), li(6,"Anne","40 kg"), li(9,"Esther","37 kg"),
        li(10,"Anja","35 kg"), li(10,"Stacy","35 kg"), li(10,"Britt","35 kg"),
        li(10,"Fiona","35 kg"), li(14,"Paula","33 kg"), li(15,"Madou","30 kg"),
        li(15,"Kirsten","30 kg"), li(17,"Anja [2]","25 kg"), li(17,"Yvonne","25 kg"),
    ])
)

# ── Challenge #52 ─────────────────────────────────────────────────────────────
c52 = acc(52, "Plank met 20 KG schijf op rug", "1 december 2023",
    note("Langste tijd wint") +
    cat("Heren") + ul([
        li(1,"Dennis","185s"), li(2,"Elsendoorn","181s"), li(3,"Ruud","165s"),
        li(4,"Sjaak","162s"), li(5,"Kees","151s"), li(6,"Peter","150s"),
        li(7,"Jorgen","147s"), li(8,"Mark","135s"), li(8,"Rene","135s"),
        li(10,"Ad","121s"), li(11,"Niels","120s"), li(11,"Elwin","120s"),
        li(13,"Rob","109s"), li(14,"Frank","81s"), li(15,"Aldo","72s"),
        li(16,"Sil","68s"), li(17,"Richard","66s"), li(18,"Jeroen","60s"),
        li(19,"Frank [2]","18s"),
    ]) +
    cat("Dames") + ul([
        li(1,"Anja","159s"), li(2,"Cynthia","123s"), li(3,"Manon","120s"),
        li(4,"Cathy","105s"), li(5,"Bente","91s"), li(6,"Britt","84s"),
        li(7,"Fleur","80s"), li(8,"Paula","68s"), li(9,"Stefanie","63s"),
        li(9,"Marije","63s"), li(11,"Nienke","58s"), li(12,"Dyonne","55s"),
        li(12,"Stacy","55s"), li(14,"Esther","50s"), li(15,"Fiona","48s"),
    ])
)

# ── Challenge #51 ─────────────────────────────────────────────────────────────
c51 = acc(51, "Sit-up met bal challenge", "23 november 2023",
    note("Meeste herhalingen wint &mdash; bal achter hoofd, voeten tikken") +
    cat("Heren") + ul([
        li(1,"Ruud","97"), li(2,"Rob","96"), li(3,"Aldo","84"), li(4,"Ad","81"),
        li(4,"Jorgen","81"), li(4,"Peter","81"), li(7,"Wouter","79"), li(8,"Theo","78"),
        li(9,"Sjaak","76"), li(10,"Kees","75"), li(11,"Dennis","73"), li(12,"Stefan","72"),
        li(13,"Jeroen","69"), li(14,"Amresh","63"), li(15,"Elwin","62"), li(16,"Frank","42"),
    ]) +
    cat("Dames") + ul([
        li(1,"Nicolette","100"), li(2,"Gwen","96"), li(3,"Bente","91"), li(4,"Manon","89"),
        li(5,"Cathy","84"), li(6,"Wendy P.","83"), li(7,"Nienke","82"), li(8,"Minou","81"),
        li(8,"Dyonne","81"), li(8,"Marije","81"), li(11,"Cynthia","77"), li(12,"Liesbeth","76"),
        li(12,"Inge","76"), li(14,"Paula","68"), li(15,"Yvonne","66"), li(16,"Esther","63"),
        li(17,"Fiona","60"), li(18,"Britt","58"), li(19,"Stefanie","55"),
    ])
)

# ── Challenge #50 ─────────────────────────────────────────────────────────────
c50 = acc(50, "Koppeltje duik challenge (ringen)", "16 november 2023",
    note("Hoogste score wint &mdash; achteruit + vooruit, elke draai = 1 punt") +
    cat("Heren") + ul([
        li(1,"Jan","48"), li(2,"Niels","44"), li(3,"Rob","43"), li(4,"Rene","30"),
        li(5,"Ruud","26"), li(6,"Aldo","22"), li(7,"Richard","18"), li(8,"Peter","17"),
        li(9,"Jorgen","12"), li(10,"Ad","10"), li(10,"Max","10"), li(12,"Stefan","6"),
        li(13,"Dennis","2"), li(14,"Frank","1"),
    ]) +
    cat("Dames") + ul([
        li(1,"Wendy P.","36"), li(2,"Charissa","30"), li(2,"Gloria","30"),
        li(4,"Manon","28"), li(4,"Fleur","28"), li(6,"Minou","26"), li(7,"Cynthia","22"),
        li(8,"Cathy","16"), li(9,"Merel","15"), li(10,"Paula","12"), li(10,"Liesbeth","12"),
        li(10,"Wendy","12"), li(10,"Bente","12"), li(14,"Joelle","10"),
    ])
)

# ── Challenge #49 ─────────────────────────────────────────────────────────────
c49 = acc(49, "Shoulder Taps challenge (2 minuten)", "9 november 2023",
    note("Meeste taps wint") +
    cat("Heren") + ul([
        li(1,"Radboud","244"), li(2,"Ruud","225"), li(3,"Rob","198"), li(4,"Ravi","198"),
        li(5,"Kevin","181"), li(6,"Jorgen","177"), li(7,"Sjaak","174"), li(8,"Ad","170"),
        li(9,"Frankly","160"), li(9,"Peter","160"), li(11,"Dennis","157"), li(11,"Jan","157"),
        li(13,"Frank M.","153"), li(14,"Rene","149"), li(15,"Sven","145"), li(16,"Mark","138"),
        li(17,"Niels","135"), li(18,"Jeroen","134"), li(19,"Elwin","130"), li(20,"Tom","99"),
        li(21,"Frank","83"), li(22,"Amresh","75"),
    ]) +
    cat("Dames") + ul([
        li(1,"Gwen","210"), li(2,"Manon","200"), li(3,"Wendy","190"), li(4,"Paula","170"),
        li(4,"Fiona","170"), li(6,"Dyonne","165"), li(7,"Cathy","163"), li(8,"Joelle","160"),
        li(9,"Liesbeth","159"), li(10,"Anne","146"), li(11,"Stacy","145"), li(12,"Merel","140"),
        li(12,"Nienke","140"), li(14,"Esther","120"), li(15,"Petra","115"), li(16,"Kim","100"),
    ])
)

# ── Challenge #48 ─────────────────────────────────────────────────────────────
c48 = acc(48, "Snatch laag/hoog challenge", "2 november 2023",
    note("Meeste snatches wint &mdash; Heren 30 KG &bull; Dames 20 KG") +
    cat("Heren") + ul([
        li(1,"Radboud","56"), li(2,"Ruud","54"), li(3,"Ro","48"), li(4,"Frank M.","46"),
        li(5,"Jan","45"), li(5,"Robert Z.","45"), li(7,"Robert Z. [2]","44"),
        li(8,"Max","40"), li(8,"Jorgen","40"), li(10,"Aldo","38"), li(11,"Stefan","31"),
        li(11,"Jeroen","31"), li(13,"Sjaak","25"), li(14,"Frank B.","19"),
    ]) +
    cat("Dames") + ul([
        li(1,"Cathy","51"), li(2,"Marije","50"), li(3,"Wendy","49"), li(4,"Cynthia","46"),
        li(5,"Bente","32"), li(6,"Paula","27"), li(7,"Ester","21"), li(8,"Sil","7"),
    ])
)

# ── Challenge #47 ─────────────────────────────────────────────────────────────
c47 = acc(47, "Bench Press (1 rep max)", "26 oktober 2023",
    note("Zwaarste gewicht wint") +
    cat("Heren") + ul([
        li(1,"Radboud","97,5 kg"), li(2,"Robert","92,5 kg"), li(3,"Rob","87,5 kg"),
        li(3,"Stefan","87,5 kg"), li(5,"Elwin","85 kg"), li(5,"Jan","85 kg"),
        li(7,"Bert","82,5 kg"), li(8,"Ruud","80 kg"), li(9,"Frank M.","77,5 kg"),
        li(10,"Dennis","75 kg"), li(10,"Aldo","75 kg"), li(12,"Pieter","72,5 kg"),
        li(13,"Jeroen","70 kg"), li(14,"Jorgen","67,5 kg"), li(15,"Bas","62,5 kg"),
        li(16,"Frank B.","60 kg"), li(16,"Frankly","60 kg"), li(18,"Sjaak","57,5 kg"),
        li(19,"Ravi","55 kg"), li(19,"Max","55 kg"), li(19,"Ivan","55 kg"),
        li(19,"Sil","55 kg"), li(23,"Ad","45 kg"), li(24,"Sven","22,5 kg"),
    ]) +
    cat("Dames") + ul([
        li(1,"Wendy","62,5 kg"), li(2,"Stefanie","52,5 kg"), li(3,"Kim","47,5 kg"),
        li(3,"Marije","47,5 kg"), li(3,"Liesbeth","47,5 kg"), li(6,"Cathy","45 kg"),
        li(6,"Wendy [2]","45 kg"), li(8,"Gaoya","42,5 kg"), li(9,"Stacy","40 kg"),
        li(9,"Esther","40 kg"), li(9,"Fleur","40 kg"), li(9,"Fiona","40 kg"),
        li(13,"Cynthia","37,5 kg"), li(13,"Nienke","37,5 kg"), li(13,"Sanne","37,5 kg"),
        li(13,"Bo","37,5 kg"), li(13,"Charissa","37,5 kg"), li(18,"Gloria","35 kg"),
        li(18,"Joelle","35 kg"), li(18,"Bente","35 kg"), li(20,"Corine","32,5 kg"),
        li(20,"Merel","32,5 kg"), li(22,"Paula","30 kg"), li(22,"Sophie","30 kg"),
        li(22,"Britt","30 kg"), li(25,"Anja","22,5 kg"), li(25,"Kirsten","22,5 kg"),
        li(25,"Madou","22,5 kg"), li(25,"Yvonne","22,5 kg"),
    ])
)

# ── Challenge #46 ─────────────────────────────────────────────────────────────
c46 = acc(46, "Verspring challenge (5&times; heen en weer)", "19 oktober 2023",
    note("Laagste aantal sprongen wint") +
    cat("Heren") + ul([
        li(1,"Kevin","20x"), li(1,"Mark","20x"), li(1,"Robert","20x"),
        li(4,"Rob","24x"), li(5,"Dennis","25x"), li(5,"Aldo","25x"),
        li(5,"Ruud","25x"), li(5,"Sil","25x"), li(5,"Ro","25x"),
        li(5,"Frank M.","25x"), li(12,"Rene","26x"), li(13,"Ad","27x"),
        li(14,"Stefan","28x"), li(15,"Sjaak","29x"), li(16,"Jan","30x"),
        li(16,"John","30x"), li(16,"Peter","30x"), li(19,"Kees","32x"),
    ]) +
    '<p style="font-size:.75rem;color:rgba(255,255,255,.4);margin:6px 0 10px;font-style:italic">* Lijst mogelijk niet volledig tussen pos. 5 en 12</p>' +
    cat("Dames") + ul([
        li(1,"Cynthia","25x"), li(1,"Gwen","25x"), li(3,"Manon","26x"),
        li(4,"Charissa","27x"), li(5,"Paula","28x"), li(5,"Marije","28x"),
        li(5,"Fleur","28x"), li(8,"Minou","29x"), li(9,"Bente","30x"),
        li(9,"Gaoya","30x"), li(9,"Dyonne","30x"), li(9,"Liesbeth","30x"),
        li(9,"Gloria","30x"), li(9,"Merel","30x"), li(9,"Esmee","30x"),
        li(16,"Britt","35x"), li(16,"Fiona","35x"), li(18,"Esther","36x"),
        li(19,"Anne","37x"),
    ])
)

# ── Challenge #45 ─────────────────────────────────────────────────────────────
c45 = acc(45, "Filthy 50 Burpees", "12 oktober 2023",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Atleten &mdash; platte burpees") + ul([
        li(1,"Gaoya","1:40"), li(2,"Cathy","2:30"), li(3,"Fleur","2:51"),
        li(4,"Merel","2:55"), li(5,"Gloria","2:56"), li(6,"Gwen","3:04"),
        li(7,"Manon","3:16"), li(8,"Mark","3:53"), li(9,"Dyonne","4:00"),
        li(10,"Robert","4:18"), li(11,"Rene","4:47"), li(12,"Stefan","4:48"),
        li(13,"Dennis","4:54"),
    ]) +
    cat("Atleten met extra levenservaring &mdash; opstapje-burpees") + ul([
        li(1,"Max","1:07"), li(2,"Marije","1:53"), li(3,"Sjaak","1:56"),
        li(4,"Stacy","2:46"), li(5,"Paula","3:13"), li(6,"Aldo","3:33"),
        li(7,"Esther","3:55"), li(8,"Ad","4:14"), li(9,"Jeroen","8:30"),
    ])
)

# ── Challenge #44 ─────────────────────────────────────────────────────────────
c44 = acc(44, "V-Sit hold (tussen 2 Bosu balance ballen)", "4 oktober 2023",
    note("Langste tijd wint") +
    cat("Heren") + ul([
        li(1,"Frank M.","2:28"), li(2,"Rob","2:22"), li(2,"Jan","2:22"),
        li(4,"Bert","2:19"), li(5,"Peter","2:01"), li(5,"Aldo","2:01"),
        li(7,"Ad","2:00"), li(8,"Radboud","1:48"), li(9,"Ruud","1:46"),
        li(10,"Dennis","1:39"), li(11,"Ivan","1:31"), li(12,"Peter [2]","1:26"),
        li(12,"Sil","1:26"), li(14,"Rene","1:18"), li(15,"Sjaak","1:05"),
        li(16,"Jeroen","1:02"), li(17,"Jurgen","1:01"), li(18,"Frank B.","0:55"),
        li(19,"Stefan","0:53"), li(20,"Cas","0:35"),
    ]) +
    cat("Dames") + ul([
        li(1,"Bente","3:18"), li(2,"Manon","3:09"), li(3,"Wendy","2:40"),
        li(4,"Gaoya","2:25"), li(5,"Liesbeth","2:21"), li(6,"Gwen","2:17"),
        li(7,"Minou","2:10"), li(8,"Paula","2:09"), li(9,"Cathy","1:45"),
        li(10,"Stacy","1:44"), li(11,"Yvonne","1:39"), li(11,"Dyonne","1:39"),
        li(13,"Marije","1:23"), li(14,"Cynthia","1:20"), li(15,"Britt","1:13"),
        li(16,"Wendy [2]","1:11"), li(17,"Jeannette","1:07"), li(18,"Nienke","1:00"),
        li(19,"Fiona","0:52"), li(20,"Esther","0:40"),
    ])
)

# ── Challenge #43 ─────────────────────────────────────────────────────────────
c43 = acc(43, "Hexa Bar Deadlift (50 reps)", "27 september 2023",
    note("Snelste tijd wint (laagste = beter) &mdash; Heren 50 KG &bull; Dames 30 KG") +
    cat("Heren") + ul([
        li(1,"Max","49s"), li(2,"Jorgen","50s"), li(2,"Bert","50s"),
        li(4,"Radboud","52s"), li(5,"Kampie","54s"), li(5,"Aldo","54s"),
        li(7,"Elwin","60s"), li(8,"John","64s"), li(9,"Ruud","65s"),
        li(10,"Rob","70s"), li(11,"Peter","71s"), li(12,"Jeroen","72s"),
        li(13,"Rene","76s"), li(14,"Sil","77s"), li(15,"Ivan","79s"),
        li(16,"JW","82s"), li(17,"Sjaak","83s"), li(18,"Ad","99s"),
        li(19,"Pieter","135s"), li(20,"Frank B.","151s"),
    ]) +
    cat("Dames") + ul([
        li(1,"Gaoya","47s"), li(2,"Wendy","51s"), li(3,"Cathy","52s"),
        li(4,"Marije","53s"), li(5,"Cynthia","54s"), li(6,"Manon","58s"),
        li(7,"Mirthe","60s"), li(8,"Bente","61s"), li(9,"Yvonne","61s"),
        li(10,"Gwen","62s"), li(10,"Wendy [2]","62s"), li(12,"Dyonne","66s"),
        li(13,"Fiona","67s"), li(14,"Jolanda","76s"), li(15,"Nienke","81s"),
        li(16,"Anja","87s"), li(17,"Stacy","90s"), li(18,"Liesbeth","135s"),
        li(18,"Paula","135s"),
    ])
)

# ── Challenge #42 ─────────────────────────────────────────────────────────────
c42 = acc(42, "3 rondjes Farmer&#39;s Walk", "21 september 2023",
    note("Snelste tijd wint (laagste = beter) &mdash; Heren 2&times;24 KG &bull; Dames 2&times;16 KG") +
    cat("Heren") + ul([
        li(1,"Max","106s"), li(2,"Radboud","109s"), li(3,"Ruud","112s"),
        li(4,"Thijs","115s"), li(5,"Kampie","118s"), li(6,"Jorgen","119s"),
        li(7,"Bert","122s"), li(8,"Rob","123s"), li(9,"Sjoerd","127s"),
        li(10,"Robert Zalando","130s"), li(11,"JW","134s"), li(12,"Theo","138s"),
        li(13,"Stijn","141s"), li(14,"Joey","143s"), li(15,"Bas","146s"),
        li(16,"Elwin","153s"), li(17,"Aldo","154s"), li(18,"Jeroen","155s"),
        li(19,"Rene","161s"), li(20,"Roderick","162s"), li(21,"Ivan","166s"),
        li(22,"Dennis","195s"), li(23,"Frank","200s"), li(24,"Ad","252s"),
        li(25,"Frankly","277s"), li(26,"Jan","378s"),
    ]) +
    cat("Dames") + ul([
        li(1,"Gaoya","111s"), li(2,"Cynthia","112s"), li(3,"Mirthe","119s"),
        li(4,"Bente","122s"), li(5,"Charissa","131s"), li(6,"Manon","134s"),
        li(6,"Gwen","134s"), li(8,"Gwen [2]","143s"), li(9,"Fleur","145s"),
        li(9,"Cathy","145s"), li(11,"Ellen","150s"), li(11,"Stacy","150s"),
        li(13,"Dyonne","155s"), li(13,"Marije","155s"), li(15,"Wendy","156s"),
        li(16,"Kim","162s"), li(17,"Liesbeth","164s"), li(18,"Anne","165s"),
        li(19,"Paula","168s"), li(20,"Nienke","169s"), li(20,"Marieke","169s"),
        li(22,"Fiona","170s"), li(22,"Merel","170s"), li(24,"Britt","171s"),
        li(25,"Joelle","175s"), li(26,"Yvonne","181s"),
    ])
)

# ── Challenge #41 ─────────────────────────────────────────────────────────────
c41 = acc(41, "Touwtje spring challenge (250x)", "13 september 2023",
    note("Snelste tijd wint (laagste = beter)") +
    cat("Heren") + ul([
        li(1,"Radboud","95s"), li(2,"Robert E.","97s"), li(3,"Stefan","101s"),
        li(4,"Dennis","107s"), li(4,"Roderick","107s"), li(6,"Sjaak","109s"),
        li(6,"Ruud","109s"), li(8,"Peter","111s"), li(9,"Frank M.","121s"),
        li(10,"Max","126s"), li(11,"Rene","127s"), li(12,"Robert","130s"),
        li(13,"Elwin","133s"), li(14,"Jeroen","141s"), li(15,"Rob","152s"),
        li(16,"Thijs","157s"), li(17,"Paul","175s"), li(18,"Frank B.","204s"),
        li(19,"Wil","211s"), li(20,"Aldo","214s"), li(21,"Ad","315s"),
    ]) +
    cat("Dames") + ul([
        li(1,"Bente","78s"), li(2,"Anne","85s"), li(3,"Wendy","90s"),
        li(4,"Gwen","95s"), li(4,"Cynthia","95s"), li(6,"Dyonne","99s"),
        li(7,"Manon","101s"), li(8,"Charissa","104s"), li(9,"Gloria","106s"),
        li(10,"Fleur","112s"), li(11,"Nienke","117s"), li(12,"Stacy","121s"),
        li(13,"Minou","124s"), li(14,"Paula","137s"), li(15,"Britt","143s"),
        li(16,"Corine","213s"), li(16,"Marieke","213s"),
    ])
)

# ── Assemble new HTML (54 → 41) ───────────────────────────────────────────────
new_challenges = (c54 + c53 + c52 + c51 + c50 + c49 + c48 + c47 +
                  c46 + c45 + c44 + c43 + c42 + c41 + "\n")

# ── Updated stats HTML ────────────────────────────────────────────────────────
NEW_STATS = """  <div class="ff-stats-grid">

    <div class="ff-stat-card">
      <h3>&#127942; Meest gewonnen (1e plaats)</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Radboud</span><span class="stat-val">9&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Gaoya</span><span class="stat-val">9&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Gwen</span><span class="stat-val">8&times; gewonnen</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Monique</span><span class="stat-val">8&times; gewonnen</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128100; Meest deelgenomen</h3>
      <div class="stat-row"><span class="stat-medal">&#129351;</span><span class="stat-name">Dennis</span><span class="stat-val">49 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129352;</span><span class="stat-name">Sjaak</span><span class="stat-val">48 challenges</span></div>
      <div class="stat-row"><span class="stat-medal">&#129353;</span><span class="stat-name">Stefan</span><span class="stat-val">46 challenges</span></div>
    </div>

    <div class="ff-stat-card">
      <h3>&#128293; Records per challenge</h3>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Paalhang</span><span class="stat-val">Jennifer &bull; 257s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Wallsit</span><span class="stat-val">Gaoya &bull; 490s</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">500m Row</span><span class="stat-val">Kevin &bull; 1:33</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Pull Ups</span><span class="stat-val">Monique &bull; 48x</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Dippen</span><span class="stat-val">Peter &bull; 180 reps</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Ski&euml;n</span><span class="stat-val">Ruud &bull; 129x</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Shoulder Taps</span><span class="stat-val">Jorgen &bull; 340 (2022)</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Deadhang</span><span class="stat-val">Kees &bull; 2:43</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Bench Press 1RM</span><span class="stat-val">Radboud &bull; 97,5 KG</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Lat Pulldown 1RM</span><span class="stat-val">Robert &bull; 71 KG</span></div>
      <div class="stat-row"><span class="stat-name" style="font-size:.8rem">Curve loopband</span><span class="stat-val">Rob &bull; 24,0 km/u</span></div>
    </div>

  </div>"""

# ── Fetch & patch page ────────────────────────────────────────────────────────
print("Ophalen pagina…")
r = requests.get(f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit", auth=auth)
r.raise_for_status()
content = r.json()["content"]["raw"]

INSERTION = "<!-- 40: Front Raise Static Hold -->"
if INSERTION not in content:
    print("FOUT: Insertion marker niet gevonden!"); exit(1)

updated = content.replace(INSERTION, new_challenges + "    " + INSERTION)

# Replace stats section
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
    print("Fout:", r2.text[:300])
