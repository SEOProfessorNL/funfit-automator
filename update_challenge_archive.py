#!/usr/bin/env python3
"""
Voegt challenges 15-40 toe aan de bestaande WordPress pagina
/challenge-van-de-week/ en herberekent de statistieken.
"""
import requests
import json

WP_URL   = "https://funfit.nu"
WP_USER  = "info@funfit.nu"
WP_PASS  = "he5r rquj NMuD hXOU KSU2 5rZa"
PAGE_ID  = 5477
auth     = (WP_USER, WP_PASS)

# ── Fetch current raw content ────────────────────────────────────────────────
print("Ophalen huidige pagina…")
r = requests.get(f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit", auth=auth)
r.raise_for_status()
content = r.json()["content"]["raw"]

# ── HTML helper ─────────────────────────────────────────────────────────────
def acc(num, title, date, inner, note=""):
    note_html = f'\n          <p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">{note}</p>' if note else ""
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
        <div class="ff-acc-inner">{note_html}
          {inner}
        </div>
      </div>
    </div>"""

def li(rank, name, score):
    return f'<li><span class="acc-rank">{rank}</span><span class="acc-name">{name}</span><span class="acc-score">{score}</span></li>'

def ul(items):
    return '<ul class="ff-acc-list">' + "".join(items) + "</ul>"

def cat(label):
    return f'<p style="font-size:.85rem;font-weight:700;margin:14px 0 4px">{label}</p>'


# ── Challenge data ───────────────────────────────────────────────────────────

c40 = acc(40, "Front Raise Static Hold", "9 aug 2023", ul([
    li(1,"Anja","140s"), li(2,"Paula","138s"), li(3,"Cynthia","104s"), li(3,"Gwen","104s"),
    li(5,"Liesbeth","96s"), li(6,"Charissa","93s"), li(6,"Stacy","93s"), li(8,"Cathy","84s"),
    li(9,"Merel","83s"), li(10,"Bert","82s"), li(11,"Anne","74s"), li(11,"Britt","74s"),
    li(13,"Roderick","73s"), li(14,"Sylvia","70s"), li(15,"Esther","69s"), li(16,"Nienke","67s"),
    li(17,"Jorgen","66s"), li(18,"Minou","64s"), li(19,"Ruud","62s"), li(19,"Corine","62s"),
    li(21,"Sjaak","61s"), li(21,"Kevin","61s"), li(23,"Dennis","60s"), li(23,"Bjorn","60s"),
    li(25,"Aldo","57s"), li(26,"Yvonne","56s"), li(27,"Stefan","55s"), li(28,"Jeroen","50s"),
    li(29,"Frank B","49s"), li(30,"Richard","45s"), li(31,"Peter","44s"), li(32,"Frankly","39s"),
    li(33,"Ivan","38s"), li(34,"Sven","32s"), li(35,"Amresh","31s"),
]))

c39 = acc(39, "Planken op 2 banken (+10KG)", "2 aug 2023", ul([
    li(1,"Cas","360s &#127942;"), li(1,"Elwin","360s &#127942;"), li(1,"Peter","360s &#127942;"),
    li(1,"Radboud","360s &#127942;"), li(1,"Britt","360s &#127942;"), li(1,"Yvonne","360s &#127942;"),
    li(1,"Cynthia","360s &#127942;"), li(1,"Anja","360s &#127942;"), li(9,"Jan","340s"),
    li(10,"Gaoya","331s"), li(11,"Jorgen","301s"), li(12,"Kees","272s"), li(13,"Bert","270s"),
    li(14,"Rene","263s"), li(15,"Sjaak","243s"), li(16,"Sil","230s"), li(17,"Ivan","214s"),
    li(18,"Minou","206s"), li(19,"Rob","197s"), li(20,"Paula","195s"), li(21,"Stefan","189s"),
    li(22,"Roderick","183s"), li(23,"Aldo","180s"), li(23,"Jeroen","180s"), li(23,"Brendan","180s"),
    li(26,"Frank M","160s"), li(27,"Dennis","155s"), li(28,"Sven","126s"), li(28,"Esther","126s"),
    li(30,"Frank B","115s"), li(31,"Amresh","110s"), li(32,"Stacy","102s"),
]))

c38 = acc(38, "Schiphol Traplopen", "27 jul 2023",
    ul([
        li(1,"Wendy","147s"), li(2,"Gwen","152s"), li(3,"Gaoya","153s"), li(4,"Manon","154s"),
        li(5,"Fleur","157s"), li(6,"Gloria","167s"), li(7,"Max","171s"), li(8,"Roderick","176s"),
        li(9,"Merel","177s"), li(10,"Esmee","179s"), li(10,"Minou","179s"), li(10,"Kevin","179s"),
        li(13,"Rob","191s"), li(14,"Tim","193s"), li(15,"Dennis","195s"), li(15,"Frank M","195s"),
        li(17,"Stefan","199s"), li(18,"Elwin","202s"), li(19,"Rene","211s"), li(20,"Sjaak","212s"),
        li(21,"Kees","215s"), li(22,"Anne","222s"), li(23,"Stacy","223s"), li(24,"Ellen","230s"),
        li(25,"Fiona","231s"), li(26,"Jeroen","236s"), li(27,"Brendan","240s"), li(28,"Ad","244s"),
        li(29,"Britt","245s"), li(30,"Paula","257s"), li(31,"Yvonne","266s"), li(32,"Frank B","277s"),
        li(33,"Esther","288s"),
    ]),
    note="Snelste tijd wint (laagste = beter)"
)

c37_inner = ul([
    li(1,"Robert","80 KG"), li(2,"Stefan","75 KG"), li(3,"Dennis","72,5 KG"),
    li(3,"Jan","72,5 KG"), li(3,"Roderick","72,5 KG"), li(6,"Elwin","70 KG"), li(6,"Rob","70 KG"),
    li(8,"Tim","65 KG"), li(8,"Bert","65 KG"), li(10,"Frank M","62,5 KG"), li(11,"Aldo","60 KG"),
    li(11,"Rene","60 KG"), li(13,"Kees","50 KG"), li(13,"Max","50 KG"), li(13,"Peter","50 KG"),
    li(13,"Sjaak","50 KG"), li(13,"Wendy","50 KG"), li(18,"Anne","42,5 KG"), li(19,"Fleur","40 KG"),
    li(19,"Marije","40 KG"), li(19,"Mirthe","40 KG"), li(19,"Sil","40 KG"), li(23,"Benthe","35 KG"),
    li(23,"Cathy","35 KG"), li(23,"Esmee","35 KG"), li(23,"Frank B","35 KG"), li(23,"Gaoya","35 KG"),
    li(28,"Charissa","32,5 KG"), li(28,"Esther","32,5 KG"), li(28,"Joelle","32,5 KG"),
    li(31,"Dyonne","30 KG"), li(31,"Gwen","30 KG"), li(31,"Minou","30 KG"), li(31,"Stacy","30 KG"),
    li(35,"Cynthia","27,5 KG"), li(35,"Merel","27,5 KG"), li(37,"Britt","25 KG"), li(37,"Gloria","25 KG"),
    li(39,"Petra","22,5 KG"), li(40,"Paula","15 KG"),
])
c37 = acc(37, "Bench Press", "20 jul 2023", c37_inner, note="Zwaarste gewicht wint")

c36_inner = (
    '<p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">120s = maximum volgehouden &#127942;</p>' +
    ul([
        li(1,"Stefan","120s &#127942;"), li(1,"Wendy","120s &#127942;"), li(1,"Anja","120s &#127942;"),
        li(1,"Bente","120s &#127942;"), li(1,"Cathy","120s &#127942;"), li(1,"Cynthia","120s &#127942;"),
        li(1,"Deborah","120s &#127942;"), li(1,"Dennis","120s &#127942;"), li(1,"Dyonne","120s &#127942;"),
        li(1,"Elwin","120s &#127942;"), li(1,"Fiona","120s &#127942;"), li(1,"Fleur","120s &#127942;"),
        li(1,"Fons","120s &#127942;"), li(1,"Gaoya","120s &#127942;"), li(1,"Gloria","120s &#127942;"),
        li(1,"Gwen","120s &#127942;"), li(1,"Jeanette","120s &#127942;"), li(1,"Jelle","120s &#127942;"),
        li(1,"Manon","120s &#127942;"), li(1,"Merel","120s &#127942;"), li(1,"Rob","120s &#127942;"),
        li(1,"Sanne","120s &#127942;"), li(23,"Jorgen","119s"), li(24,"Peter","117s"),
        li(25,"Jan","113s"), li(25,"Wouter","113s"), li(27,"Esther","108s"), li(28,"Tim","101s"),
        li(29,"Kampie","99s"), li(29,"Sjoerd","99s"), li(31,"Roderick","96s"), li(32,"Inge","89s"),
        li(33,"Britt","81s"), li(34,"Anne","79s"), li(35,"Paula","75s"), li(36,"Kees","72s"),
        li(37,"Pieter","70s"), li(38,"Max","67s"), li(39,"Ellen","56s"), li(40,"Sjaak","55s"),
        li(41,"Rene","49s"), li(42,"Jeroen","38s"), li(43,"Ad","31s"), li(43,"Petra","31s"),
        li(43,"Stacy","31s"), li(46,"Wilma","29s"), li(47,"Frank B","28s"), li(48,"Frank M","26s"),
    ])
)
c36 = acc(36, "Balans op blauwe bosu bal", "15 jul 2023", c36_inner)

c35 = acc(35, "Curve loopband (km/u)", "5 jul 2023",
    ul([
        li(1,"Rob","24,0"), li(2,"Bink","23,7"), li(3,"Ruud","23,2"), li(4,"Ivan","22,9"),
        li(5,"Sil","22,1"), li(6,"Stefan","21,9"), li(7,"Aldo","21,8"), li(8,"Frank M","21,7"),
        li(9,"Max","21,2"), li(9,"Dennis","21,2"), li(11,"Stijn","20,9"), li(12,"Roderick","20,8"),
        li(13,"Radboud","20,7"), li(14,"Bente","20,4"), li(15,"Jorgen","20,2"), li(16,"Kees","19,9"),
        li(17,"Marije","19,7"), li(17,"Jeanet","19,7"), li(17,"Manon","19,7"), li(20,"John","19,6"),
        li(21,"Sjaak","18,5"), li(22,"Gaoya","18,3"), li(23,"Dyonne","17,8"), li(24,"Stacy","17,5"),
        li(25,"Gwen","17,1"), li(25,"Minou","17,1"), li(27,"Cynthia","16,9"), li(28,"Liesbeth","16,7"),
        li(29,"Brit","16,4"), li(30,"Esther","16,2"), li(31,"Fiona","16,1"), li(32,"Ad","15,1"),
        li(33,"Paula","13,5"), li(34,"Frank B","12,5"),
    ]),
    note="Hoogste snelheid wint"
)

c34 = acc(34, "Vierkant hinkelen", "28 jun 2023",
    ul([
        li(1,"Sil","59s"), li(2,"Max","63s"), li(3,"Rob","71s"), li(4,"Kevin","73s"),
        li(5,"Ruud","76s"), li(6,"Roderick","77s"), li(7,"Radboud","81s"), li(8,"Jan","86s"),
        li(9,"Stefan","87s"), li(10,"Bente","91s"), li(11,"Sjoerd","93s"), li(12,"Dennis","97s"),
        li(13,"Frank","99s"), li(14,"Elwin","102s"), li(15,"Jeanet","121s"), li(16,"Amresh","135s"),
        li(17,"Sjaak","140s"), li(18,"Kees","142s"), li(19,"Yvonne","149s"), li(20,"Paula","179s"),
        li(21,"Frank","199s"),
    ]),
    note="Snelste tijd wint (laagste = beter)"
)

c33_inner = (
    cat("Dames 2&times;8 KG") +
    ul([
        li(1,"Monique","140"), li(2,"Wendy","130"), li(3,"Manon","122"),
        li(4,"Gwen","119"), li(4,"Gaoya","119"), li(6,"Esmee","118"), li(7,"Cathy","116"),
        li(8,"Charissa","113"), li(8,"Mikal","113"), li(10,"Bente","109"), li(11,"Marije","107"),
        li(11,"Merel","107"), li(13,"Liesbeth","104"), li(14,"Minou","103"), li(14,"Dyonne","103"),
        li(16,"Joelle","100"), li(17,"Britt","96"), li(17,"Gloria","96"), li(19,"Esther","92"),
        li(19,"Yvon","92"), li(21,"Anja","90"), li(21,"Kirsten","90"), li(23,"Anne","87"),
        li(24,"Paula","80"),
    ]) +
    cat("Heren 2&times;16 KG") +
    ul([
        li(1,"Ruud","132"), li(1,"Radboud","132"), li(3,"Kevin","126"), li(4,"Rob","122"),
        li(5,"Bert","110"), li(6,"Kees","108"), li(7,"Stefan","104"), li(8,"Frank M","103"),
        li(8,"Sjaak","103"), li(10,"Rene","100"), li(11,"Dennis","98"), li(12,"Frank M","96"),
        li(12,"Pieter","96"), li(14,"Elwin","92"), li(15,"Roderick","89"), li(16,"Peter","82"),
        li(17,"Ivan","79"),
    ])
)
c33 = acc(33, "Step up the Step", "22 jun 2023", c33_inner)

c32 = acc(32, "Rondje hoofdveld FC Lisse", "15 jun 2023",
    ul([
        li(1,"Ivan","59,69s"), li(2,"Stijn","62,32s"), li(3,"Rob","67,60s"),
        li(4,"Roderick","69,66s"), li(5,"Ruud","70,20s"), li(6,"Wouter","70,76s"),
        li(7,"Dennis","71,00s"), li(8,"Stefan","72,04s"), li(9,"Radboud","72,12s"),
        li(10,"Max","72,98s"), li(11,"Gwen","73,40s"), li(12,"Bert","77,30s"),
        li(13,"Charissa","79,50s"), li(14,"Manon","79,80s"), li(15,"Jorgen","82,26s"),
        li(16,"Gaoya","83,16s"), li(17,"Aldo","84,10s"), li(18,"Wendy","85,38s"),
        li(19,"Pieter","89,51s"), li(20,"Frank M","89,80s"), li(21,"Sjaak","92,25s"),
        li(22,"Dyonne","93,60s"), li(22,"Lotte","93,60s"), li(24,"Cathy","93,96s"),
        li(25,"Minou","95,20s"), li(26,"Bente","95,28s"), li(27,"Marije","97,30s"),
        li(28,"Merel","98,10s"), li(29,"Joelle","98,30s"), li(30,"Stacy","103,88s"),
        li(31,"Jeroen","104,60s"), li(32,"Elwin","106,80s"), li(33,"Yvonne","107,58s"),
        li(34,"Jeanette","110,00s"), li(35,"Liesbeth","118,00s"), li(36,"Fiona","120,80s"),
        li(37,"Anne","121,00s"), li(38,"Petra","147,80s"),
    ]),
    note="Snelste tijd wint (laagste = beter)"
)

c31_inner = (
    '<p style="font-size:.8rem;color:rgba(255,255,255,.55);margin:0 0 10px">240s = maximum volgehouden &#127942;</p>' +
    ul([
        li(1,"Bert","240s &#127942;"), li(1,"Rene","240s &#127942;"), li(1,"Radboud","240s &#127942;"),
        li(1,"Manon","240s &#127942;"), li(1,"Liesbeth","240s &#127942;"), li(1,"Kees","240s &#127942;"),
        li(1,"Gwen","240s &#127942;"), li(1,"Gaoya","240s &#127942;"), li(1,"Frank M","240s &#127942;"),
        li(1,"Elwin","240s &#127942;"), li(1,"Cathy","240s &#127942;"), li(1,"Bente","240s &#127942;"),
        li(1,"Monique","240s &#127942;"), li(14,"Rob","236s"), li(15,"Britt","224s"),
        li(16,"Jeanette","219s"), li(17,"Sjaak","201s"), li(18,"Bjorn","185s"), li(19,"Dyonne","184s"),
        li(20,"Ruud","182s"), li(21,"Jorgen","177s"), li(22,"Minou","170s"), li(23,"Petra","160s"),
        li(24,"Aldo","155s"), li(25,"Kevin","154s"), li(26,"Stefan","145s"), li(27,"Jaap","142s"),
        li(28,"Dennis","132s"), li(29,"Roderick","121s"), li(30,"Marije","117s"), li(31,"Paula","115s"),
        li(32,"Yvonne","92s"), li(33,"Stacy","88s"), li(34,"Frank B","81s"), li(35,"Jeroen","73s"),
    ])
)
c31 = acc(31, "Copenhagen Plank", "8 jun 2023", c31_inner)

c30 = acc(30, "Burpee + Verspring", "31 mei 2023",
    ul([
        li(1,"Gaoya","73m"), li(2,"Gwen","70m"), li(2,"Manon","70m"), li(4,"Ruud","67m"),
        li(5,"Radboud","63m"), li(6,"Marije","60m"), li(6,"Bert","60m"), li(8,"Cathy","56m"),
        li(9,"Max","54m"), li(10,"Dyonne","51m"), li(11,"Rob","50m"), li(12,"Stefan","49m"),
        li(13,"Wendy","48m"), li(13,"Roderick","48m"), li(15,"Rene","46m"), li(15,"Sjoerd","46m"),
        li(17,"Liesbeth","45m"), li(18,"Aldo","43m"), li(19,"Dennis","37m"), li(20,"Bente","35m"),
        li(21,"Sjaak","33m"), li(22,"Elwin","30m"), li(22,"Kees","30m"), li(24,"Jeroen","29m"),
        li(24,"Yvonne","29m"), li(26,"Fiona","28m"), li(27,"Britt","25m"), li(28,"Frank B","22m"),
        li(29,"Petra","20m"), li(30,"Paula","18m"),
    ]),
    note="Langste afstand wint"
)

c29 = acc(29, "Kijk eens wat ik kan", "24 mei 2023",
    ul([
        li(1,"Sven","152s"), li(2,"Kees","149s"), li(3,"Gloria","147s"), li(4,"Bert","145s"),
        li(5,"Charissa","134s"), li(6,"Sjoerd","130s"), li(7,"Manon","116s"), li(8,"Ivan","111s"),
        li(9,"Radboud","109s"), li(10,"Rob","108s"), li(11,"Cynthia","107s"), li(12,"Kevin","105s"),
        li(13,"Fleur","104s"), li(13,"Gwen","104s"), li(15,"Max","102s"), li(16,"Merel","100s"),
        li(17,"Frank M","91s"), li(18,"Jorgen","82s"), li(19,"Sjaak","80s"), li(20,"Rene","78s"),
        li(21,"Gaoya","75s"), li(22,"Wendy","70s"), li(23,"Liesbeth","69s"), li(24,"Noor","68s"),
        li(25,"Bente","62s"), li(25,"Joelle","62s"), li(27,"Yvonne","55s"), li(28,"Ruud","51s"),
        li(29,"Paula","49s"), li(30,"Stefan","46s"), li(31,"Elwin","35s"), li(32,"Petra","33s"),
        li(33,"Frank B","31s"), li(34,"Jeroen","24s"), li(35,"Cathy","23s"), li(36,"Dennis","22s"),
        li(37,"Anne","18s"), li(38,"Esther","11s"),
    ])
)

c28 = acc(28, "500m Roeien (herhaling)", "17 mei 2023",
    ul([
        li(1,"Kevin","1:33"), li(2,"Rob","1:34"), li(2,"Jeroen","1:34"), li(2,"Frank M","1:34"),
        li(5,"Ruud","1:37"), li(5,"Max","1:37"), li(5,"Radboud","1:37"), li(8,"Ivan","1:40"),
        li(9,"Mike","1:41"), li(10,"Jorgen","1:43"), li(11,"Sjaak","1:44"), li(11,"Bert","1:44"),
        li(13,"Pieter","1:45"), li(13,"Stefan","1:45"), li(15,"Dennis","1:47"), li(16,"Jan","1:50"),
        li(17,"Kees","1:51"), li(17,"Stacy","1:51"), li(19,"Dyonne","1:53"), li(19,"Bente","1:53"),
        li(21,"Wendy","1:55"), li(21,"Cynthia","1:55"), li(23,"Fleur","1:56"), li(24,"Rene","1:57"),
        li(24,"Gwen","1:57"), li(26,"Manon","1:58"), li(26,"Gaoya","1:58"), li(26,"Cathy","1:58"),
        li(26,"Esmee","1:58"), li(26,"Charissa","1:58"), li(31,"Sanne","2:00"), li(31,"Merel","2:00"),
        li(33,"Esther","2:05"), li(34,"Sjoerd","2:07"), li(35,"Jeanette","2:09"), li(36,"Inge","2:12"),
        li(37,"Fiona","2:13"), li(37,"Gloria","2:13"), li(39,"Anja","2:20"), li(39,"Yvonne","2:20"),
        li(41,"Britt","2:22"), li(42,"Amresh","2:25"), li(43,"Sylvia","2:29"), li(44,"Frank B","2:38"),
        li(44,"Paula","2:38"), li(46,"Liesbeth","2:40"),
    ]),
    note="Snelste tijd wint (laagste = beter)"
)

c27_inner = (
    cat("Dames 30 KG") +
    ul([
        li(1,"Gwen","78"), li(2,"Wendy","74"), li(3,"Manon","72"), li(4,"Esther","70"),
        li(5,"Stacy","66"), li(6,"Bente","63"), li(7,"Liesbeth","60"), li(8,"Cynthia","59"),
        li(9,"Paula","30"),
    ]) +
    cat("Heren 40 KG") +
    ul([
        li(1,"Frank M","95"), li(2,"Pieter","88"), li(3,"Aldo","82"), li(4,"Stefan","79"),
        li(5,"Rob","77"), li(6,"Roderick","76"), li(7,"Ruud","75"), li(7,"Jeroen","75"),
        li(9,"Kees","65"), li(10,"Sjaak","60"), li(10,"Elwin","60"), li(12,"Dennis","59"),
        li(13,"Frank","41"),
    ])
)
c27 = acc(27, "Lat Pulldown", "10 mei 2023", c27_inner)

c26_inner = (
    cat("Dames 3 KG") +
    ul([
        li(1,"Monique","56"), li(2,"Gaoya","52"), li(3,"Liesbeth","46"), li(4,"Fleur","42"),
        li(5,"Cynthia","36"), li(6,"Joelle","35"), li(7,"Dyonne","31"), li(7,"Marije","31"),
        li(9,"Manon","30"), li(9,"Jeanette","30"), li(9,"Gloria","30"), li(12,"Britt","29"),
        li(13,"Anne","26"), li(14,"Charissa","25"), li(15,"Paula","21"), li(16,"Stacy","20"),
        li(17,"Bente","15"), li(17,"Fiona","15"), li(17,"Merel","15"), li(20,"Esther","12"),
        li(21,"Cathy","8"),
    ]) +
    cat("Heren 4 KG") +
    ul([
        li(1,"Radboud","107"), li(2,"Aldo","43"), li(3,"Ruud","40"), li(3,"Peter","40"),
        li(5,"Max","33"), li(6,"Robert","32"), li(7,"Dennis","31"), li(7,"Pieter","31"),
        li(9,"Stefan","30"), li(10,"Bert","29"), li(11,"Frank M","28"), li(12,"Rene","27"),
        li(13,"Roderick","26"), li(14,"Ivan","25"), li(15,"Sjaak","24"), li(16,"Bas","23"),
        li(16,"Kees","23"), li(18,"Jorgen","14"), li(19,"Frank B","11"),
    ])
)
c26 = acc(26, "Leg Raises till Failure", "4 mei 2023", c26_inner)

c25_inner = (
    cat("Dames 16 KG") +
    ul([
        li(1,"Manon","1:24"), li(2,"Gwen","1:26"), li(3,"Dyonne","1:31"), li(4,"Bente","1:36"),
        li(5,"Esmee","1:37"), li(6,"Sanne","1:40"), li(7,"Wendy","1:45"), li(7,"Merel","1:45"),
        li(9,"Anne","1:46"), li(10,"Gaoya","1:49"), li(11,"Charissa","1:50"), li(12,"Stacy","1:53"),
        li(13,"Liesbeth","1:54"), li(14,"Petra","1:57"), li(15,"Fleur","1:58"), li(16,"Gloria","2:01"),
        li(17,"Marije","2:02"), li(18,"Joelle","2:03"), li(19,"Anja","2:22"), li(20,"Paula","2:25"),
        li(21,"Britt","2:48"), li(22,"Fiona","2:50"),
    ]) +
    cat("Heren 24 KG") +
    ul([
        li(1,"Kevin","1:16"), li(2,"Rob","1:18"), li(3,"Radboud","1:26"), li(4,"Frank M","1:31"),
        li(5,"Ruud","1:33"), li(6,"Stefan","1:34"), li(7,"Max","1:37"), li(8,"Bert","1:45"),
        li(9,"Roderick","1:47"), li(10,"Dennis","1:49"), li(11,"Ivan","1:52"), li(12,"Kees","1:53"),
        li(13,"Rene","1:56"), li(14,"Elwin","1:59"), li(14,"Sjaak","1:59"), li(16,"Aldo","2:00"),
        li(17,"Jeroen","2:02"), li(18,"Jan","2:04"),
    ])
)
c25 = acc(25, "10&times; Farmer&#39;s Walk heen en weer", "26 apr 2023", c25_inner,
    note="Snelste tijd wint (laagste = beter)")

c24_inner = (
    cat("Dames") +
    ul([
        li(1,"Monique","46"), li(2,"Gwen","35"), li(3,"Gaoya","29"), li(4,"Bente","28"),
        li(5,"Liesbeth","20"), li(5,"Cynthia","20"), li(7,"Manon","19"), li(8,"Dyonne","14"),
        li(9,"Paula","11"), li(10,"Brit","10"), li(11,"Charissa","7"), li(12,"Esther","5"),
        li(13,"Wendy","4"), li(14,"Anne","1"),
    ]) +
    cat("Heren") +
    ul([
        li(1,"Aldo","45"), li(2,"Radboud","43"), li(3,"Tim","42"), li(4,"Jorgen","30"),
        li(5,"Rob","29"), li(6,"Ben","24"), li(7,"Ruud","23"), li(8,"Rene","17"),
        li(9,"Sjaak","16"), li(9,"Kees","16"), li(11,"Kevin","15"), li(11,"Frank","15"),
        li(13,"Dennis","12"), li(14,"Frank M","11"), li(15,"Peter","10"),
    ])
)
c24 = acc(24, "Hangend aan rek benen over foamrol", "11 apr 2023", c24_inner)

c23 = acc(23, "Staande Plank Golfbal Jongleren", "2 feb 2023",
    ul([
        li(1,"Ben","138"), li(2,"Sjaak","121"), li(3,"Mark","103"), li(4,"Max","98"),
        li(4,"Monique","98"), li(6,"Robert","97"), li(7,"Tom","92"), li(8,"Mike","90"),
        li(9,"Richard","88"), li(10,"Gaoya","84"), li(11,"Aldo","76"), li(12,"Dennis","75"),
        li(13,"Gloria","71"), li(14,"Rene","65"), li(15,"Peter","62"), li(15,"Jeroen","62"),
        li(17,"Gwen","61"), li(18,"Marije","60"), li(18,"Pieter","60"), li(20,"Manon","56"),
        li(21,"Fleur","52"), li(22,"Kim","50"), li(22,"Sjaak","50"), li(22,"Liesbeth","50"),
        li(25,"Esmee","47"), li(26,"Brit","46"), li(27,"Frank","41"), li(27,"Sjoerd","41"),
        li(29,"Cynthia","37"), li(29,"Charissa","37"), li(31,"Liset","33"), li(32,"Jurgen","29"),
        li(33,"Esther","27"), li(33,"Merel","27"), li(35,"Joelle","26"), li(36,"Anne","23"),
        li(37,"Romy","22"),
    ])
)

c22 = acc(22, "Golfbal Putten Bosu Balance", "17 jan 2023",
    ul([
        li(1,"Stefan","41"), li(2,"Manon","34"), li(2,"Frank","34"), li(4,"Kees","33"),
        li(5,"Mark","32"), li(5,"Jurgen","32"), li(7,"Gwen","27"), li(8,"Ruud","26"),
        li(8,"Peter","26"), li(10,"Rob","24"), li(11,"Tessa","21"), li(11,"Aldo","21"),
        li(13,"Cynthia","20"), li(14,"Dennis","18"), li(14,"Pieter","18"), li(16,"Roderick","17"),
        li(17,"Monique","16"), li(18,"Sjaak","14"), li(18,"Gaoya","14"), li(18,"Esther","14"),
        li(18,"Cathy","14"), li(22,"Brit","13"), li(22,"Bente","13"), li(24,"Minou","12"),
        li(25,"Gloria","11"), li(26,"Esmee","6"), li(26,"Merel","6"), li(26,"Ivan","6"),
        li(29,"Marije","4"), li(30,"Dyonne","3"), li(31,"Charissa","2"), li(31,"Rene","2"),
        li(33,"Joelle","1"), li(34,"Liesbeth","&minus;4"),
    ])
)

c21_inner = (
    cat("Heren 6 KG") +
    ul([
        li(1,"Frank","182s"), li(2,"Pieter","145s"), li(3,"Roderick","142s"), li(4,"Stefan","138s"),
        li(5,"Sjaak","132s"), li(6,"Kees","128s"), li(7,"Ruud","125s"), li(8,"Jorgen","123s"),
        li(9,"Rob","121s"), li(10,"Jeroen","118s"), li(11,"Aldo","115s"), li(12,"Max","108s"),
        li(13,"Dennis","88s"), li(14,"Peter","68s"),
    ]) +
    cat("Dames 4 KG") +
    ul([
        li(1,"Jeanet","195s"), li(2,"Lotte","193s"), li(3,"Gaoya","173s"), li(4,"Monique","138s"),
        li(5,"Manon","135s"), li(6,"Cynthia","134s"), li(7,"Cathy","129s"), li(8,"Liesbeth","128s"),
        li(9,"Marije","117s"), li(10,"Britt","112s"), li(11,"Minou","94s"), li(12,"Wendy","88s"),
        li(13,"Benthe","79s"), li(14,"Petra","41s"),
    ])
)
c21 = acc(21, "Zittende Dumbbell Hold", "13 dec 2022", c21_inner)

c20 = acc(20, "Maximale Deadhang", "3 dec 2022",
    ul([
        li(1,"Kees","2:43"), li(2,"Rafael","2:14"), li(3,"Frank","1:47"), li(4,"Bente","1:31"),
        li(5,"Gwen","1:20"), li(6,"Cynthia","1:18"), li(7,"Aldo","1:17"), li(8,"Max","1:15"),
        li(9,"Wendy","1:13"), li(10,"Manon","1:12"), li(11,"Petra","1:09"), li(12,"Gaoya","1:04"),
        li(13,"Joelle","1:03"), li(14,"Peter","1:01"), li(14,"Dennis","1:01"), li(16,"Esmee","0:58"),
        li(17,"Esther","0:56"), li(18,"Monique","0:54"), li(19,"Jeroen","0:53"), li(20,"Cathy","0:50"),
        li(21,"Dyonne","0:36"), li(22,"Tamara","0:34"), li(23,"Roderick","0:30"), li(23,"Britt","0:30"),
        li(25,"Anne","0:17"),
    ])
)

c19 = acc(19, "180s Shoulder Taps", "18 okt 2022",
    ul([
        li(1,"Jorgen","340"), li(2,"Gaoya","314"), li(3,"Aldo","306"), li(4,"Kees","300"),
        li(5,"Cynthia","295"), li(6,"Jeanet","284"), li(7,"Manon","279"), li(8,"Ruud","278"),
        li(9,"Pieter","268"), li(10,"Gwen","267"), li(11,"Sjaak","265"), li(12,"Ad","262"),
        li(13,"Danny","250"), li(13,"Cathy","250"), li(13,"Roderick","250"), li(16,"Rob","239"),
        li(17,"Peter","238"), li(18,"Dennis","225"), li(19,"Stefan","218"), li(20,"Britt","193"),
        li(21,"Bente","189"), li(22,"Frank","185"), li(23,"Marije","181"), li(24,"Liesbeth","180"),
        li(24,"Pascal","180"), li(26,"Dyonne","172"), li(27,"Maarten","165"), li(28,"Lotte","164"),
        li(29,"Jeroen","148"),
    ])
)

c18_inner = (
    cat("Heren 10 KG") +
    ul([
        li(1,"Ruud","103"), li(2,"Rob","98"), li(3,"Jorgen","93"), li(4,"Aldo","86"),
        li(4,"Sjaak","86"), li(6,"Pieter","84"), li(7,"Dennis","83"), li(8,"Rene","75"),
        li(8,"Roderick","75"), li(10,"Ad","73"), li(11,"Stefan","72"), li(12,"Jeroen","70"),
        li(13,"Maarten","50"),
    ]) +
    cat("Dames 4 KG") +
    ul([
        li(1,"Gaoya","99"), li(2,"Marije","97"), li(2,"Minou","97"), li(4,"Dyonne","92"),
        li(4,"Cathy","92"), li(6,"Manon","90"), li(7,"Cynthia","86"), li(8,"Bente","83"),
        li(9,"Jeanet","76"), li(10,"Esther","65"), li(11,"Petra","55"),
    ])
)
c18 = acc(18, "Slamball Challenge (180s)", "3 okt 2022", c18_inner)

c17 = acc(17, "Achteruit touwtje springen (200x)", "26 sep 2022",
    ul([
        li(1,"Cynthia","1:46"), li(2,"Bente","2:09"), li(3,"Cathy","2:10"), li(4,"Petra","2:14"),
        li(5,"Monique","2:16"), li(6,"Marije","2:17"), li(7,"Gaoya","2:20"), li(8,"Manon","2:28"),
        li(9,"Jorgen","2:31"), li(10,"Ruud","2:36"), li(11,"Dyonne","2:42"), li(12,"Gwen","2:46"),
        li(12,"Minou","2:46"), li(14,"Sjaak","3:01"), li(15,"Jeanet","3:17"), li(16,"Max","3:27"),
        li(17,"Esther","3:31"), li(18,"Rob","3:32"), li(19,"Peter","3:55"), li(20,"Dennis","3:57"),
        li(21,"Ad","4:01"), li(22,"Pieter","4:18"), li(23,"Stefan","5:17"), li(24,"Roderick","7:10"),
    ]),
    note="Snelste tijd wint (laagste = beter)"
)

c16_inner = (
    cat("Heren 20 KG") +
    ul([
        li(1,"Jorgen","1:45"), li(2,"Rob","1:47"), li(3,"Ruud","1:48"), li(4,"Ad","1:59"),
        li(5,"Aldo","2:00"), li(6,"Stefan","2:02"), li(6,"Pieter","2:02"), li(8,"Frank","2:03"),
        li(8,"Tim","2:03"), li(10,"Sjaak","2:08"), li(11,"Sven","2:20"), li(12,"Roderick","2:21"),
        li(13,"Dennis","2:23"),
    ]) +
    cat("Dames 12 KG") +
    ul([
        li(1,"Gwen","1:51"), li(2,"Minou","1:54"), li(2,"Jeanet","1:54"), li(4,"Lotte","1:55"),
        li(5,"Marije","1:56"), li(6,"Bente","1:57"), li(6,"Cathy","1:57"), li(8,"Gaoya","1:59"),
        li(9,"Manon","2:09"), li(10,"Dyonne","2:15"), li(11,"Petra","2:49"),
    ])
)
c16 = acc(16, "50&times; Kettlebell 8-vorm squat", "16 sep 2022", c16_inner,
    note="Snelste tijd wint (laagste = beter)")

c15 = acc(15, "Halterstang Challenge (100x)", "5 sep 2022",
    ul([
        li(1,"Ruud","80s"), li(2,"Rob","92s"), li(3,"Kees","99s"), li(4,"Minou","103s"),
        li(5,"Monique","113s"), li(6,"Cathy","117s"), li(7,"Frank","125s"), li(8,"Peter","131s"),
        li(9,"Pieter","132s"), li(10,"Jorgen","138s"), li(11,"Aldo","147s"), li(12,"Stefan","148s"),
        li(13,"Sabrine","152s"), li(14,"Gaoya","166s"), li(15,"Sjaak","167s"), li(16,"Britt","169s"),
        li(17,"Dennis","200s"), li(18,"Cynthia","201s"), li(19,"Manon","226s"), li(20,"Dyonne","227s"),
        li(21,"Sven","233s"), li(22,"Roderick","236s"), li(23,"Petra","340s"), li(24,"Bente","353s"),
        li(25,"Rene","412s"),
    ]),
    note="Snelste tijd wint (laagste = beter)"
)

# ── Assemble new challenges HTML (40 → 15) ──────────────────────────────────
new_html = (c40 + c39 + c38 + c37 + c36 + c35 + c34 + c33 + c32 + c31 +
            c30 + c29 + c28 + c27 + c26 + c25 + c24 + c23 + c22 + c21 +
            c20 + c19 + c18 + c17 + c16 + c15 + "\n")

# ── Updated statistics HTML ──────────────────────────────────────────────────
NEW_STATS = """\
  <div class="ff-stats-grid">

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

# ── Inject into page content ─────────────────────────────────────────────────
INSERTION_MARKER = "<!-- 14: Lunge Challenge -->"
if INSERTION_MARKER not in content:
    print(f"FOUT: Marker '{INSERTION_MARKER}' niet gevonden in paginacontent!")
    exit(1)

# Insert new challenges before challenge 14
updated = content.replace(INSERTION_MARKER, new_html + "    " + INSERTION_MARKER)

# Replace old stats grid with new one
import re
updated = re.sub(
    r'<div class="ff-stats-grid">.*?</div>\s*</div>\s*<!-- /accordion -->',
    NEW_STATS + '\n\n  </div><!-- /accordion -->',
    updated,
    flags=re.DOTALL
)

# ── Push to WordPress ────────────────────────────────────────────────────────
print("Bijwerken WordPress pagina…")
r2 = requests.post(
    f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}",
    auth=auth,
    json={"content": updated, "status": "draft"}
)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    d = r2.json()
    print(f"✓ Pagina bijgewerkt (ID {d['id']}, status: {d['status']})")
    print(f"  Preview: https://funfit.nu/?page_id={PAGE_ID}")
    print(f"  Edit:    {WP_URL}/wp-admin/post.php?post={PAGE_ID}&action=edit")
else:
    print("Fout:", r2.text[:400])
