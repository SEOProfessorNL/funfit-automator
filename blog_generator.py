#!/usr/bin/env python3
"""
Blog Automator voor funfit.nu
Haalt trending SEO keywords op, genereert een blogpost met Claude,
maakt een afbeelding met DALL-E, en plant de post in op WordPress.
"""

import os
import sys
import json
import logging
import requests
from io import BytesIO
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import anthropic
from openai import OpenAI

# ── Config ───────────────────────────────────────────────────────────
load_dotenv()

DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WP_URL = os.getenv("WP_URL", "https://funfit.nu")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

NL_TZ = ZoneInfo("Europe/Amsterdam")
TOPIC_QUEUE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topic_queue.json")

# ── Logging ──────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/blog_log.txt", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ── Helpers ──────────────────────────────────────────────────────────
def next_friday_9am():
    """Bereken de eerstvolgende vrijdag om 09:00 NL-tijd."""
    now = datetime.now(NL_TZ)
    days_ahead = (4 - now.weekday()) % 7  # 4 = vrijdag
    if days_ahead == 0 and now.hour >= 9:
        days_ahead = 7
    target = now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
    return target


# ── Stap 0: Topic Queue – Check geplande onderwerpen ─────────────────
def pop_queued_topic():
    """Haal het eerste onderwerp uit topic_queue.json en verwijder het.
    Returns None als de queue leeg is of niet bestaat."""
    if not os.path.exists(TOPIC_QUEUE_FILE):
        log.info("   📋 Geen topic_queue.json gevonden, skip.")
        return None

    try:
        with open(TOPIC_QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log.warning(f"   ⚠️  Kon topic_queue.json niet lezen: {e}")
        return None

    if not queue:
        log.info("   📋 Topic queue is leeg, val terug op trending keywords.")
        return None

    # Pak het eerste item
    topic = queue.pop(0)
    log.info(f"   📋 Queued topic gevonden: \"{topic.get('title_hint', '?')}\"")

    # Schrijf de resterende queue terug
    with open(TOPIC_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    log.info(f"   📋 {len(queue)} topics resterend in queue.")

    return topic


def commit_queue_update():
    """Commit en push de bijgewerkte topic_queue.json naar GitHub."""
    import subprocess
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        subprocess.run(["git", "-C", repo_dir, "add", "topic_queue.json"], check=True, capture_output=True)
        result = subprocess.run(
            ["git", "-C", repo_dir, "diff", "--cached", "--quiet"],
            capture_output=True
        )
        if result.returncode != 0:  # Er zijn staged changes
            subprocess.run(
                ["git", "-C", repo_dir, "commit", "-m", "chore: pop topic from queue"],
                check=True, capture_output=True
            )
            subprocess.run(
                ["git", "-C", repo_dir, "push"],
                check=True, capture_output=True
            )
            log.info("   📋 topic_queue.json gecommit en gepusht naar GitHub.")
        else:
            log.info("   📋 Geen wijzigingen in topic_queue.json om te committen.")
    except subprocess.CalledProcessError as e:
        log.warning(f"   ⚠️  Kon topic_queue.json niet committen: {e}")


# ── Stap 1: DataForSEO – Trending keywords ──────────────────────────
def fetch_trending_keywords():
    """Haal trending SEO-gerelateerde zoekwoorden op via DataForSEO."""
    log.info("📡 Stap 1: Trending keywords ophalen via DataForSEO...")

    # Roteer tussen fitness-gerelateerde seed keywords
    seed_keywords = [
        "fitness", "hyrox", "personal training", "krachttraining",
        "workout", "voeding sport", "afvallen sportschool",
        "spieropbouw", "conditie opbouwen", "functioneel trainen",
    ]
    # Kies een seed keyword op basis van de week van het jaar
    week_number = datetime.now(NL_TZ).isocalendar()[1]
    seed = seed_keywords[week_number % len(seed_keywords)]
    log.info(f"   🔑 Seed keyword: {seed}")

    url = "https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live"
    payload = [
        {
            "keyword": seed,
            "language_code": "nl",
            "location_code": 2528,  # Nederland
            "limit": 20,
            "filters": [
                "keyword_data.keyword_info.search_volume", ">", 100
            ],
            "order_by": ["keyword_data.keyword_info.search_volume,desc"],
        }
    ]

    response = requests.post(
        url,
        json=payload,
        auth=(DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status_code") != 20000:
        raise RuntimeError(f"DataForSEO fout: {data.get('status_message')}")

    items = data["tasks"][0]["result"][0].get("items", [])
    keywords = []
    for item in items[:10]:
        kw_data = item.get("keyword_data", {})
        kw_info = kw_data.get("keyword_info", {})
        keywords.append(
            {
                "keyword": kw_data.get("keyword", ""),
                "search_volume": kw_info.get("search_volume", 0),
                "competition": kw_info.get("competition", 0),
            }
        )

    log.info(f"   ✅ {len(keywords)} keywords gevonden")
    for kw in keywords[:5]:
        log.info(f"      - {kw['keyword']} (vol: {kw['search_volume']})")

    return keywords


# ── Stap 2: Claude – Blogpost genereren ─────────────────────────────
def _build_blogpost_prompt(keywords, queued_topic=None):
    """Bouw de prompt voor blogpost-generatie."""
    keyword_list = ", ".join(kw["keyword"] for kw in keywords[:5])

    today = datetime.now(NL_TZ).strftime("%d %B %Y")

    # Als er een queued topic is, voeg specifieke instructies toe
    topic_instruction = ""
    if queued_topic:
        topic_instruction = f"""
SPECIFIEK ONDERWERP (heeft prioriteit boven trending keywords):
- Titel richting: {queued_topic.get('title_hint', '')}
- Focus keyword: {queued_topic.get('focus_keyword', '')}
- Gerelateerde keywords: {', '.join(queued_topic.get('seed_keywords', []))}
- Instructies: {queued_topic.get('notes', '')}

Schrijf het artikel over dit specifieke onderwerp. Gebruik de trending keywords hieronder alleen als inspiratie voor extra context of als je ze natuurlijk kunt verwerken.
"""

    return f"""Je schrijft voor funfit.nu, de website van FunFit — een sportschool in Lisse
gericht op personal training, groepslessen, HYROX-training en een gezonde levensstijl.
Vandaag is het {today}. Schrijf een diepgaande, waardevolle Nederlandse blogpost van MINIMAAL 1200 woorden.

{topic_instruction}TRENDING KEYWORDS (kies het meest interessante onderwerp voor een sportschool-publiek):
{keyword_list}

OVER FUNFIT:
- Sportschool in Lisse met focus op personal training en groepslessen
- Specialisatie in HYROX-training en functioneel trainen
- Eigenaar: Mark van Marrewijk
- Doelgroep: sporters van alle niveaus die resultaat willen boeken

KWALITEITSEISEN:
- Dit moet een artikel zijn waar sporters en fitnessliefhebbers daadwerkelijk iets van leren
- Geen oppervlakkige opsommingen — ga de diepte in met concrete trainingsvoorbeelden en praktische tips
- Onderbouw claims met sportwetenschap of trainingsdata waar mogelijk
- Geef actionable tips die de lezer direct kan toepassen in de sportschool
- Beschrijf oefeningen, schema's of voedingstips stap-voor-stap waar relevant
- Benoem veelgemaakte fouten en hoe je ze voorkomt
- Maak het relevant voor zowel beginners als gevorderden

SCHRIJFSTIJL:
- Nederlandstalig, informeel maar professioneel (je/jij-vorm)
- Schrijf vanuit het perspectief van een ervaren personal trainer / sportschool
- Natuurlijke, menselijke schrijfstijl — geen AI-achtige zinnen of clichés
- Varieer in zinslengte, gebruik af en toe spreektaal
- Deel praktijkervaringen: "Wat we vaak zien bij onze leden...", "In de praktijk..."
- Durf een mening te geven en stelling te nemen

STRUCTUUR:
- Minstens 4-5 H2 subkoppen die het artikel logisch opdelen
- Mix van paragrafen, lijsten, en eventueel een vergelijkingstabel in HTML
- Begin met een sterke hook die het probleem of de vraag schetst
- Eindig met een concrete conclusie of actieplan

STRUCTUUR (geef dit EXACT terug in dit JSON-formaat):
{{
  "title": "Pakkende H1 titel (max 60 tekens, bevat hoofdkeyword)",
  "meta_description": "SEO meta description (max 155 tekens, wekt nieuwsgierigheid)",
  "slug": "url-vriendelijke-slug",
  "content": "De volledige HTML blogpost met <h2> subkoppen, <p> paragrafen, <ul>/<li> lijsten, eventueel <table> waar relevant. MINIMAAL 1200 woorden. Voeg ergens in de tekst deze link natuurlijk toe: <a href=\\"https://funfit.nu/personal-training\\">personal training bij FunFit</a>. Gebruik GEEN <h1> tag (die komt van de titel). Gebruik GEEN inline styles of style attributen — de styling wordt automatisch toegepast door het theme. Lever schone, semantische HTML.",
  "focus_keyword": "het hoofdkeyword van de post",
  "dalle_prompt": "Een Engelse prompt voor DALL-E om een professionele, energieke blogheader afbeelding te genereren die past bij het onderwerp. Stijl: modern fitness/sportschool thema, dynamisch, motiverend. Geen tekst in de afbeelding."
}}

BELANGRIJK: Het artikel moet MINIMAAL 1200 woorden bevatten. Lever kwaliteit, geen vulling.
Geef ALLEEN de JSON terug, geen andere tekst."""


def _parse_json_response(response_text):
    """Parse JSON uit een LLM response, strip eventuele code fences."""
    text = response_text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    return json.loads(text)


import re


def style_blog_content(html):
    """Wrap blogpost in het FunFit dark design met nav, styled content en footer."""

    WRAPPER_CSS = (
        '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900'
        '&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet"><style>'
        "body.single-post #page > #masthead,body.single-post .site-header,body.single-post .qodef-page-header,"
        "body.single-post .qodef-mobile-header,body.single-post #colophon,body.single-post .site-footer,"
        "body.single-post .qodef-page-footer,body.single-post .qodef-footer-top-holder,"
        "body.single-post .qodef-footer-bottom-holder,body.single-post .qodef-title-holder,"
        "body.single-post .qodef-title,body.single-post .entry-header,body.single-post .page-header,"
        "body.single-post .qodef-back-to-top,body.single-post .breadcrumbs,body.single-post .breadcrumb,"
        "body.single-post .page-title-wrap,body.single-post .page-title-bar,"
        "body.single-post .qodef-blog-holder .qodef-blog-list,body.single-post .qodef-comment-holder,"
        "body.single-post .qodef-related-posts-holder,body.single-post .qodef-blog-single-navigation,"
        "body.single-post .qodef-sidebar,body.single-post aside,"
        "body.single-post .qodef-menu-area,body.single-post .qodef-main-menu,"
        "body.single-post .qodef-logo-wrapper,body.single-post .qodef-mobile-header-holder,"
        "body.single-post .qodef-mobile-nav,body.single-post .qodef-mobile-menu-opener,"
        "body.single-post .qodef-fixed-wrapper,body.single-post .qodef-top-bar"
        "{display:none!important;visibility:hidden!important;height:0!important;max-height:0!important;"
        "overflow:hidden!important;opacity:0!important;pointer-events:none!important;"
        "position:absolute!important;clip:rect(0,0,0,0)!important}"
        "\n/* Post title & meta — dark theme */\n"
        "body.single-post .entry-title.qodef-post-title{color:#fff!important;font-family:'Barlow Condensed',sans-serif!important;"
        "font-weight:800!important;font-size:clamp(2rem,5vw,3.2rem)!important;line-height:1.1!important;"
        "letter-spacing:.5px!important;margin:0 0 20px!important;max-width:800px!important;padding:0 24px!important;"
        "margin-left:auto!important;margin-right:auto!important}"
        "body.single-post .qodef-post-info-top{max-width:800px!important;margin:0 auto 32px!important;"
        "padding:0 24px!important;display:flex!important;align-items:center!important;gap:16px!important;flex-wrap:wrap!important}"
        "body.single-post .qodef-post-info-author{display:inline-flex!important;align-items:center!important;gap:6px!important}"
        "body.single-post .qodef-post-info-author-image{display:none!important}"
        "body.single-post .qodef-post-info-author a,body.single-post .qodef-post-info-author span,"
        "body.single-post .qodef-post-info-author-text{color:#FFFFFF!important;"
        "font-family:'Barlow Condensed',sans-serif!important;font-weight:600!important;"
        "text-transform:uppercase!important;letter-spacing:1.5px!important;font-size:.85rem!important}"
        "body.single-post .qodef-post-info-author a:hover{color:#baca28!important}"
        "body.single-post .qodef-post-info-date,body.single-post .qodef-post-info-date a{color:#baca28!important;"
        "font-family:'Barlow Condensed',sans-serif!important;font-weight:700!important;"
        "text-transform:uppercase!important;letter-spacing:2px!important;font-size:.85rem!important}"
        "body.single-post .qodef-post-info-category,body.single-post .qodef-post-info-comments,"
        "body.single-post .qodef-post-info-comments-holder,body.single-post .qodef-post-info-bottom{display:none!important}"
        "body.single-post .saboxplugin-wrap{max-width:800px!important;margin:0 auto 40px!important;padding:24px!important;"
        "background:#111!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:14px!important}"
        "body.single-post .saboxplugin-wrap .saboxplugin-socials{background:transparent!important;"
        "border-top:1px solid rgba(255,255,255,.08)!important}"
        "body.single-post .saboxplugin-authorname a{color:#baca28!important;"
        "font-family:'Barlow Condensed',sans-serif!important;font-weight:700!important;"
        "text-transform:uppercase!important;letter-spacing:1px!important}"
        "body.single-post .saboxplugin-desc,body.single-post .saboxplugin-desc p{color:#e6e6e6!important}"
        "body.single-post .saboxplugin-gravatar img{border-radius:50%!important}"
        "\nhtml,body{padding:0!important;margin:0!important;background:#0A0A0A!important}"
        ".qodef-wrapper,.qodef-wrapper-inner,.qodef-content,.qodef-content-inner,.qodef-container,"
        ".qodef-container-inner,.qodef-page-content-holder,.qodef-full-width,.qodef-grid-col-12,"
        ".qodef-grid-col-8,.qodef-grid,.site-content,.entry-content,.content-area,#primary,#content,"
        ".page-content,.site-main,main,.wrapper,.container-fluid{padding:0!important;margin:0!important;"
        "max-width:100%!important;width:100%!important;background:transparent!important;float:none!important}"
        ".ff-root,.ff-root *{box-sizing:border-box}"
        ":root{--green:#baca28;--blue:#0081a3;--dark:#0A0A0A;--white:#FFFFFF;--gray-900:#111111;"
        "--gray-400:#FFFFFF;--gray-200:#FFFFFF;--radius:14px;--container:1240px;"
        "--shadow:0 20px 60px rgba(0,0,0,.35);--transition:all .25s ease}"
        "*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}"
        "body{font-family:'Barlow',system-ui,sans-serif;background:var(--dark);color:var(--white);"
        "line-height:1.65;font-size:17px;overflow-x:hidden;-webkit-font-smoothing:antialiased}"
        "h1,h2,h3,h4{font-family:'Barlow Condensed',sans-serif;font-weight:800;line-height:1.15;letter-spacing:.5px;color:var(--white)}"
        "p{max-width:75ch}a{color:inherit;text-decoration:none}img{max-width:100%;display:block}"
        ".container{max-width:var(--container);margin:0 auto;padding:0 24px}"
        ".brand-fun{color:var(--blue)}.brand-fit{color:var(--green)}"
        ".ff-overlay-nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:transparent;"
        "transition:background .3s ease,backdrop-filter .3s ease}"
        ".ff-overlay-nav.scrolled{background:rgba(13,26,15,.92);backdrop-filter:blur(14px);box-shadow:0 4px 24px rgba(0,0,0,.35)}"
        ".ff-nav-inner{max-width:var(--container);margin:0 auto;padding:18px 24px;display:flex;"
        "align-items:center;justify-content:space-between;gap:24px}"
        ".ff-nav-logo{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:1.7rem;"
        "text-transform:uppercase;letter-spacing:1px;color:#fff;white-space:nowrap}"
        ".ff-nav-links{list-style:none;display:flex;align-items:center;gap:30px;margin:0;padding:0}"
        ".ff-nav-links>li{position:relative}"
        ".ff-nav-links a{color:#fff!important;text-decoration:none;font-family:'Barlow Condensed',sans-serif;"
        "font-weight:700;text-transform:uppercase;letter-spacing:1.2px;font-size:.95rem;padding:10px 0;"
        "display:inline-block;transition:color .2s}.ff-nav-links a:hover{color:#c8e63c!important}"
        ".ff-nav-links .ff-submenu{position:absolute;top:100%;left:0;min-width:230px;"
        "background:rgba(13,26,15,.96);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.08);"
        "border-radius:10px;padding:10px 0;margin:0;list-style:none;opacity:0;visibility:hidden;"
        "transform:translateY(8px);transition:all .2s ease;box-shadow:0 20px 50px rgba(0,0,0,.45)}"
        ".ff-nav-links>li:hover>.ff-submenu{opacity:1;visibility:visible;transform:translateY(0)}"
        ".ff-submenu li{display:block}.ff-submenu a{display:block;padding:10px 20px;font-size:.9rem;"
        "letter-spacing:1px;white-space:nowrap}.ff-submenu a:hover{background:rgba(200,230,60,.08)}"
        ".ff-nav-toggle{display:none;background:transparent;border:none;width:44px;height:44px;cursor:pointer;padding:0;color:#fff}"
        ".ff-nav-toggle span{display:block;width:26px;height:2px;background:#fff;margin:5px auto;"
        "transition:all .25s ease;border-radius:2px}"
        "@media(max-width:960px){.ff-nav-toggle{display:block}.ff-nav-links{display:none}}"
        "@media(max-width:768px){.ff-overlay-nav.is-open{position:fixed!important;top:0!important;"
        "left:0!important;right:0!important;width:100%!important;height:100vh!important;"
        "background:#0d1a0f!important;z-index:99999!important;overflow-y:auto!important}"
        ".ff-overlay-nav.is-open .ff-nav-inner{flex-direction:column;align-items:stretch;padding:20px 0 40px}"
        ".ff-overlay-nav.is-open .ff-nav-logo,.ff-overlay-nav.is-open .ff-nav-toggle{position:absolute;top:18px}"
        ".ff-overlay-nav.is-open .ff-nav-logo{left:24px}.ff-overlay-nav.is-open .ff-nav-toggle{right:24px}"
        ".ff-overlay-nav.is-open .ff-nav-links{display:flex!important;flex-direction:column;gap:0;"
        "padding:70px 0 20px;margin:0;list-style:none;width:100%}"
        ".ff-overlay-nav.is-open .ff-nav-links>li{display:block!important;width:100%;"
        "border-bottom:1px solid rgba(255,255,255,.08)}"
        ".ff-overlay-nav.is-open .ff-nav-links a{display:block!important;padding:16px 24px!important;"
        "font-size:18px!important;width:100%}"
        ".ff-overlay-nav.is-open .ff-submenu{position:static!important;opacity:1!important;"
        "visibility:visible!important;transform:none!important;background:rgba(255,255,255,.03)!important;"
        "border:none!important;box-shadow:none!important;padding:0!important;margin:0!important;list-style:none}"
        ".ff-overlay-nav.is-open .ff-submenu a{padding:12px 24px 12px 40px!important;font-size:15px!important}}"
        "\n.ff-article{max-width:800px;margin:0 auto;padding:40px 24px 80px}"
        ".ff-article h2{color:var(--green);font-size:clamp(1.5rem,3vw,2rem);margin:48px 0 16px}"
        ".ff-article h3{color:var(--blue);font-size:clamp(1.2rem,2vw,1.5rem);margin:36px 0 12px}"
        ".ff-article p{color:var(--gray-200);margin:0 0 18px;font-size:1.05rem;line-height:1.75}"
        ".ff-article ul,.ff-article ol{color:var(--gray-200);margin:0 0 24px 20px;font-size:1.05rem;line-height:1.75}"
        ".ff-article li{margin-bottom:8px}"
        ".ff-article a{color:var(--green);border-bottom:1px solid rgba(186,202,40,.3);transition:border-color .2s}"
        ".ff-article a:hover{border-color:var(--green)}"
        ".ff-article strong{color:var(--white)}"
        ".ff-article table{width:100%;border-collapse:collapse;margin:24px 0}"
        ".ff-article th{background:var(--gray-900);color:var(--green);padding:12px 16px;text-align:left;"
        "font-family:'Barlow Condensed',sans-serif;font-weight:700;text-transform:uppercase;"
        "letter-spacing:1px;font-size:.9rem;border-bottom:2px solid var(--green)}"
        ".ff-article td{padding:12px 16px;color:var(--gray-200);border-bottom:1px solid rgba(255,255,255,.06)}"
        ".ff-article img{border-radius:var(--radius);margin:24px 0;box-shadow:var(--shadow)}"
        ".ff-article blockquote{border-left:4px solid var(--green);padding:16px 24px;margin:24px 0;"
        "background:rgba(186,202,40,.05);border-radius:0 var(--radius) var(--radius) 0}"
        ".ff-post-cta{background:linear-gradient(135deg,var(--green) 0%,#d4e33a 100%);color:var(--dark);"
        "text-align:center;padding:80px 24px}"
        ".ff-post-cta h2{color:var(--dark)!important;margin-bottom:20px;text-transform:uppercase;"
        "font-family:'Barlow Condensed',sans-serif;font-weight:800}"
        ".ff-post-cta p{color:rgba(10,10,10,.8);margin:0 auto 36px;font-size:1.2rem}"
        ".ff-post-cta .btn{display:inline-flex;align-items:center;gap:10px;padding:18px 32px;border-radius:12px;"
        "font-family:'Barlow Condensed',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;"
        "font-size:1.05rem;background:var(--dark);color:var(--white);border:2px solid var(--dark);transition:all .25s ease}"
        ".ff-post-cta .btn:hover{background:transparent;color:var(--dark)}"
        ".footer{background:var(--dark);padding:60px 0 40px;border-top:1px solid rgba(255,255,255,.06);text-align:center}"
        ".footer__logo{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:1.8rem;"
        "text-transform:uppercase;margin-bottom:12px}"
        ".footer p{margin:0 auto;color:var(--gray-400);font-size:.95rem}"
        ".footer__links{list-style:none;display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin:20px 0;padding:0}"
        ".footer__links a{color:var(--gray-400);font-family:'Barlow Condensed',sans-serif;font-weight:600;"
        "text-transform:uppercase;letter-spacing:1px;font-size:.85rem;transition:color .2s}"
        ".footer__links a:hover{color:var(--green)}"
        ":focus-visible{outline:3px solid var(--green);outline-offset:3px;border-radius:6px}"
        "</style>"
    )

    NAV = (
        '<nav class="ff-overlay-nav" id="ffOverlayNav" aria-label="Hoofdnavigatie"><div class="ff-nav-inner">'
        '<a href="https://funfit.nu/" class="ff-nav-logo"><span class="brand-fun">FUN</span>'
        '<span class="brand-fit">FIT</span> LISSE</a>'
        '<button class="ff-nav-toggle" id="ffNavToggle" aria-expanded="false" aria-label="Menu openen">'
        '<span></span><span></span><span></span></button>'
        '<ul class="ff-nav-links" id="ffNavLinks">'
        '<li><a href="https://funfit.nu/">Home</a></li>'
        '<li class="has-submenu"><a href="https://funfit.nu/personal-training/">Personal Training</a>'
        '<ul class="ff-submenu"><li><a href="https://funfit.nu/bootcamp-lisse/">Bootcamp</a></li>'
        '<li><a href="https://funfit.nu/small-group-training/">Small Group Training</a></li></ul></li>'
        '<li><a href="https://funfit.nu/hyrox-lisse/">Hyrox</a></li>'
        '<li class="has-submenu"><a href="https://funfit.nu/sportschool-lisse/">Sportschool</a>'
        '<ul class="ff-submenu"><li><a href="https://funfit.nu/sportschool-hillegom/">Hillegom</a></li>'
        '<li><a href="https://funfit.nu/sportschool-sassenheim/">Sassenheim</a></li>'
        '<li><a href="https://funfit.nu/sportschool-noordwijkerhout/">Noordwijkerhout</a></li>'
        '<li><a href="https://funfit.nu/sportschool-voorhout/">Voorhout</a></li>'
        '<li><a href="https://funfit.nu/sportschool-noordwijk/">Noordwijk</a></li></ul></li>'
        '<li><a href="https://funfit.nu/inschrijven/">Inschrijven</a></li>'
        '<li><a href="https://funfit.nu/contact/">Contact</a></li></ul>'
        '</div></nav>'
    )

    CTA = (
        '<div class="ff-post-cta">'
        '<h2>Ook Trainen Bij FunFit?</h2>'
        '<p>Kom langs voor een gratis kennismakingsgesprek. Onze trainers laten je graag zien wat we te bieden hebben.</p>'
        '<a href="https://funfit.nu/inschrijven/" class="btn">Schrijf Je In &rarr;</a>'
        '</div>'
    )

    FOOTER = (
        '<footer class="footer"><div class="container">'
        '<div class="footer__logo"><span class="brand-fun">FUN</span><span class="brand-fit">FIT</span> LISSE</div>'
        '<p style="color:var(--green);font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:.85rem;'
        'text-transform:uppercase;letter-spacing:2px;margin:8px auto 24px">'
        '&#9733; Enige Hyrox Approved Gym In De Bollenstreek</p>'
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:40px;max-width:900px;margin:0 auto 40px;text-align:left">'
        '<div><p style="color:var(--green);font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:.8rem;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:12px">Training</p>'
        '<ul style="list-style:none;padding:0;margin:0">'
        '<li style="padding:4px 0"><a href="https://funfit.nu/personal-training/" style="color:var(--gray-400);font-size:.9rem">Personal Training</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/hyrox-lisse/" style="color:var(--gray-400);font-size:.9rem">Hyrox Training</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/bootcamp-lisse/" style="color:var(--gray-400);font-size:.9rem">Bootcamp</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/small-group-training/" style="color:var(--gray-400);font-size:.9rem">Small Group Training</a></li></ul></div>'
        '<div><p style="color:var(--green);font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:.8rem;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:12px">Locaties</p>'
        '<ul style="list-style:none;padding:0;margin:0">'
        '<li style="padding:4px 0"><a href="https://funfit.nu/sportschool-hillegom/" style="color:var(--gray-400);font-size:.9rem">Hillegom</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/sportschool-sassenheim/" style="color:var(--gray-400);font-size:.9rem">Sassenheim</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/sportschool-noordwijkerhout/" style="color:var(--gray-400);font-size:.9rem">Noordwijkerhout</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/sportschool-voorhout/" style="color:var(--gray-400);font-size:.9rem">Voorhout</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/sportschool-noordwijk/" style="color:var(--gray-400);font-size:.9rem">Noordwijk</a></li></ul></div>'
        '<div><p style="color:var(--green);font-family:\'Barlow Condensed\',sans-serif;font-weight:700;font-size:.8rem;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:12px">Info</p>'
        '<ul style="list-style:none;padding:0;margin:0">'
        '<li style="padding:4px 0"><a href="https://funfit.nu/over-funfit/" style="color:var(--gray-400);font-size:.9rem">Over FunFit</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/blog/" style="color:var(--gray-400);font-size:.9rem">Blog</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/inschrijven/" style="color:var(--gray-400);font-size:.9rem">Inschrijven</a></li>'
        '<li style="padding:4px 0"><a href="https://funfit.nu/contact/" style="color:var(--gray-400);font-size:.9rem">Contact</a></li>'
        '<li style="padding:4px 0"><a href="tel:+31623224068" style="color:var(--gray-400);font-size:.9rem">06 23224068</a></li></ul></div>'
        '</div>'
        '<div style="border-top:1px solid rgba(255,255,255,.06);padding-top:24px">'
        '<p>Spekkelaan 1, 2161 GH Lisse &middot; '
        '<a href="https://www.facebook.com/FunFit.nu" style="color:var(--gray-400)">Facebook</a> &middot; '
        '<a href="https://www.instagram.com/funfitlisse/" style="color:var(--gray-400)">Instagram</a></p>'
        '<p style="margin-top:12px;font-size:.85rem">&copy; 2026 FunFit Lisse. Alle rechten voorbehouden.</p>'
        '</div></div></footer>'
    )

    JS = (
        "<script>(function(){var nav=document.getElementById('ffOverlayNav'),"
        "toggle=document.getElementById('ffNavToggle');"
        "if(toggle&&nav){toggle.addEventListener('click',function(){"
        "var open=nav.classList.toggle('is-open');"
        "toggle.setAttribute('aria-expanded',open?'true':'false');"
        "document.body.style.overflow=open?'hidden':''});"
        "nav.querySelectorAll('.ff-nav-links a').forEach(function(a){"
        "a.addEventListener('click',function(){if(nav.classList.contains('is-open')){"
        "nav.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');"
        "document.body.style.overflow=''}})})}"
        "var onScroll=function(){if(!nav)return;if(window.scrollY>40)"
        "nav.classList.add('scrolled');else nav.classList.remove('scrolled')};"
        "window.addEventListener('scroll',onScroll,{passive:true});onScroll()})();</script>"
    )

    return (
        f"{WRAPPER_CSS}\n"
        f'<div class="ff-root">\n'
        f"{NAV}\n"
        f'<div style="padding-top:100px;background:var(--dark)">\n'
        f'<div class="ff-article">\n'
        f"{html}\n"
        f"</div>\n"
        f"</div>\n"
        f"{CTA}\n"
        f"{FOOTER}\n"
        f"</div>\n"
        f"{JS}"
    )


def generate_blogpost(keywords, queued_topic=None):
    """Genereer een Nederlandse blogpost. Probeert eerst Claude, fallback naar GPT-4o."""
    log.info("✍️  Stap 2: Blogpost genereren...")

    prompt = _build_blogpost_prompt(keywords, queued_topic=queued_topic)

    # Probeer Claude eerst
    try:
        log.info("   🔄 Probeer Claude API...")
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8096,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = message.content[0].text
        post_data = _parse_json_response(response_text)
        log.info("   ✅ Blogpost gegenereerd met Claude")

    except Exception as e:
        log.warning(f"   ⚠️  Claude niet beschikbaar: {e}")
        log.info("   🔄 Fallback naar OpenAI GPT-4o...")

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.7,
        )
        response_text = response.choices[0].message.content
        post_data = _parse_json_response(response_text)
        log.info("   ✅ Blogpost gegenereerd met GPT-4o")

    log.info(f"   📰 Titel: \"{post_data['title']}\"")
    log.info(f"   📝 Focus keyword: {post_data['focus_keyword']}")
    word_count = len(post_data["content"].split())
    log.info(f"   📏 Woordentelling: ~{word_count} woorden")

    # Pas inline styles toe zodat WordPress-thema kleuren niet overschrijft
    post_data["content"] = style_blog_content(post_data["content"])

    return post_data


# ── Stap 3: DALL-E – Afbeelding genereren ───────────────────────────
def generate_image(dalle_prompt):
    """Genereer een blogheader afbeelding met DALL-E 3."""
    log.info("🎨 Stap 3: Afbeelding genereren met DALL-E 3...")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt

    log.info(f"   ✅ Afbeelding gegenereerd")
    log.info(f"   🖼️  Revised prompt: {revised_prompt[:100]}...")

    # Download de afbeelding
    img_response = requests.get(image_url, timeout=60)
    img_response.raise_for_status()

    log.info(f"   📥 Afbeelding gedownload ({len(img_response.content) / 1024:.0f} KB)")
    return img_response.content


# ── Stap 4a: WordPress – Afbeelding uploaden ────────────────────────
def upload_image_to_wp(image_bytes, filename="blog-header.png"):
    """Upload afbeelding naar WordPress media library."""
    log.info("📤 Stap 4a: Afbeelding uploaden naar WordPress...")

    url = f"{WP_URL}/wp-json/wp/v2/media"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/png",
    }

    import time
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                url,
                headers=headers,
                data=image_bytes,
                auth=(WP_USER, WP_APP_PASSWORD),
                timeout=120,
            )
            response.raise_for_status()
            media = response.json()
            break
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            log.warning(f"   ⚠️  Upload poging {attempt}/{max_retries} mislukt: {e}")
            if attempt < max_retries:
                wait = attempt * 10
                log.info(f"   ⏳ Wacht {wait}s voor volgende poging...")
                time.sleep(wait)
            else:
                raise

    media_id = media["id"]
    media_url = media.get("source_url", "")

    log.info(f"   ✅ Afbeelding geüpload (ID: {media_id})")
    log.info(f"   🔗 URL: {media_url}")

    return media_id


# ── Stap 4b: WordPress – Post publiceren ────────────────────────────
def create_wp_post(post_data, media_id, publish_date=None):
    """Maak een WordPress post aan en publiceer direct. Retry bij SSL/connectie-fouten."""
    log.info("📝 Stap 4b: WordPress post aanmaken en publiceren...")

    url = f"{WP_URL}/wp-json/wp/v2/posts"
    payload = {
        "title": post_data["title"],
        "content": post_data["content"],
        "status": "publish",
        "slug": post_data["slug"],
        "excerpt": post_data["meta_description"],
    }
    if media_id:
        payload["featured_media"] = media_id

    import time
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                url,
                json=payload,
                auth=(WP_USER, WP_APP_PASSWORD),
                timeout=60,
            )
            response.raise_for_status()
            wp_post = response.json()
            break
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError) as e:
            log.warning(f"   ⚠️  Poging {attempt}/{max_retries} mislukt: {e}")
            if attempt < max_retries:
                wait = attempt * 10
                log.info(f"   ⏳ Wacht {wait}s voor volgende poging...")
                time.sleep(wait)
            else:
                log.error(f"   ❌ Alle {max_retries} pogingen mislukt")
                raise

    post_id = wp_post["id"]
    post_link = wp_post.get("link", "")

    log.info(f"   ✅ Post aangemaakt (ID: {post_id})")
    log.info(f"   🔗 Link: {post_link}")
    log.info(f"   📅 Ingepland: {date_str}")

    return wp_post


# ── Stap 5: LinkedIn – Post genereren en plaatsen ────────────────────
def get_linkedin_member_id():
    """Haal LinkedIn member ID (sub) op via userinfo endpoint."""
    log.info("   🔍 LinkedIn member ID ophalen via userinfo...")
    response = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}"},
        timeout=15,
    )
    log.info(f"   🔍 Userinfo status: {response.status_code}")
    if response.status_code != 200:
        log.error(f"   ❌ Userinfo response headers: {dict(response.headers)}")
        log.error(f"   ❌ Userinfo response body: {response.text}")
        response.raise_for_status()
    data = response.json()
    log.info(f"   🔍 Userinfo keys: {list(data.keys())}")
    return data["sub"]


def generate_linkedin_post(post_data):
    """Genereer een LinkedIn post via Claude."""
    log.info("💬 Stap 5a: LinkedIn post genereren met Claude...")

    blog_url = f"https://funfit.nu/{post_data['slug']}/"

    prompt = f"""Schrijf een pakkende LinkedIn post in het Nederlands.

BLOGPOST INFO:
- Titel: {post_data['title']}
- Onderwerp: {post_data['focus_keyword']}
- URL: {blog_url}

JE SCHRIJFT ALS:
Mark van Marrewijk, eigenaar van FunFit — een sportschool in Lisse
gespecialiseerd in personal training, groepslessen en HYROX-training.

VEREISTEN:
- Max 1300 tekens (inclusief hashtags)
- Nederlandstalig
- Professioneel maar persoonlijk — schrijf als een sportschool-eigenaar en trainer die zijn kennis deelt
- Begin met een pakkende opening (hook) die aandacht trekt
- Vermeld de blogtitel en link naar het artikel
- Eindig met 3-5 relevante hashtags zoals #Fitness #PersonalTraining #HYROX #FunFit #Sportschool
- Gebruik witregels voor leesbaarheid
- Geen emoji-overload, max 3-4 emoji's
- Natuurlijke schrijfstijl, geen AI-achtige zinnen

Geef ALLEEN de LinkedIn post tekst terug, geen JSON of andere opmaak."""

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    linkedin_text = message.content[0].text.strip()
    log.info(f"   ✅ LinkedIn post gegenereerd ({len(linkedin_text)} tekens)")
    return linkedin_text


def post_to_linkedin(text):
    """Plaats een post op LinkedIn via de UGC Posts API."""
    log.info("📤 Stap 5b: Plaatsen op LinkedIn...")

    member_id = get_linkedin_member_id()
    log.info(f"   👤 LinkedIn member: {member_id}")

    payload = {
        "author": f"urn:li:person:{member_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    log.info(f"   🔍 Payload: {json.dumps(payload, indent=2)}")
    log.info(f"   🔍 Token (eerste 10 chars): {LINKEDIN_ACCESS_TOKEN[:10]}...")

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        json=payload,
        headers={
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        timeout=30,
    )

    log.info(f"   🔍 Response status: {response.status_code}")
    log.info(f"   🔍 Response headers: {dict(response.headers)}")
    log.info(f"   🔍 Response body: {response.text}")

    if response.status_code not in (200, 201):
        log.error(f"   ❌ LinkedIn API fout ({response.status_code}): {response.text}")
        response.raise_for_status()

    result = response.json()
    post_id = result.get("id", "onbekend")
    log.info(f"   ✅ LinkedIn post geplaatst (ID: {post_id})")
    return result


# ── Individuele tests ────────────────────────────────────────────────
def test_dataforseo():
    """Test DataForSEO API verbinding."""
    log.info("🧪 TEST: DataForSEO API...")
    try:
        keywords = fetch_trending_keywords()
        log.info("   ✅ DataForSEO API werkt!\n")
        return keywords
    except Exception as e:
        log.error(f"   ❌ DataForSEO fout: {e}\n")
        return None


def test_claude():
    """Test Claude API verbinding."""
    log.info("🧪 TEST: Claude API...")
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": "Zeg 'hallo' in het Nederlands."}],
        )
        log.info(f"   ✅ Claude API werkt! Response: {msg.content[0].text}\n")
        return True
    except Exception as e:
        log.error(f"   ❌ Claude API fout: {e}\n")
        return False


def test_openai():
    """Test OpenAI/DALL-E API verbinding."""
    log.info("🧪 TEST: OpenAI API...")
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        # Simpele test zonder afbeelding te genereren (bespaart kosten)
        models = client.models.list()
        dalle3 = any(m.id == "dall-e-3" for m in models.data)
        if dalle3:
            log.info("   ✅ OpenAI API werkt! DALL-E 3 beschikbaar.\n")
        else:
            log.warning("   ⚠️  OpenAI API werkt maar DALL-E 3 niet gevonden.\n")
        return True
    except Exception as e:
        log.error(f"   ❌ OpenAI API fout: {e}\n")
        return False


def test_wordpress():
    """Test WordPress REST API verbinding."""
    log.info("🧪 TEST: WordPress API...")
    try:
        url = f"{WP_URL}/wp-json/wp/v2/posts?per_page=1"
        response = requests.get(
            url,
            auth=(WP_USER, WP_APP_PASSWORD),
            timeout=15,
        )
        response.raise_for_status()
        log.info(f"   ✅ WordPress API werkt! Status: {response.status_code}\n")
        return True
    except Exception as e:
        log.error(f"   ❌ WordPress API fout: {e}\n")
        return False


def test_linkedin():
    """Test LinkedIn API verbinding."""
    log.info("🧪 TEST: LinkedIn API...")
    if not LINKEDIN_ACCESS_TOKEN:
        log.error("   ❌ LINKEDIN_ACCESS_TOKEN niet ingesteld in .env\n")
        return False
    try:
        member_id = get_linkedin_member_id()
        log.info(f"   ✅ LinkedIn API werkt! Member ID: {member_id}\n")
        return True
    except Exception as e:
        log.error(f"   ❌ LinkedIn API fout: {e}\n")
        return False


# ── Main ─────────────────────────────────────────────────────────────
def main():
    log.info("=" * 60)
    log.info("🚀 Blog Automator voor funfit.nu gestart")
    log.info("=" * 60)

    # Controleer environment variables (LinkedIn is optioneel)
    missing = []
    for var in ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD", "ANTHROPIC_API_KEY",
                "OPENAI_API_KEY", "WP_USER", "WP_APP_PASSWORD"]:
        if not os.getenv(var):
            missing.append(var)
    if missing:
        log.error(f"❌ Ontbrekende environment variabelen: {', '.join(missing)}")
        sys.exit(1)
    if not os.getenv("LINKEDIN_ACCESS_TOKEN"):
        log.warning("⚠️  LINKEDIN_ACCESS_TOKEN niet ingesteld — LinkedIn post wordt overgeslagen")

    if "--test" in sys.argv:
        log.info("🧪 Testmodus: elke API-verbinding apart testen\n")
        test_dataforseo()
        test_claude()
        test_openai()
        test_wordpress()
        test_linkedin()
        log.info("🧪 Tests afgerond.")
        return

    if "--linkedin-only" in sys.argv:
        log.info("📣 LinkedIn-only modus")
        # Haal de slug en titel op via extra argumenten of gebruik de laatste WP post
        title = None
        slug = None
        for arg in sys.argv:
            if arg.startswith("--title="):
                title = arg.split("=", 1)[1]
            elif arg.startswith("--slug="):
                slug = arg.split("=", 1)[1]

        if not title or not slug:
            log.info("   Laatste gepubliceerde post ophalen van WordPress...")
            url = f"{WP_URL}/wp-json/wp/v2/posts?status=publish&per_page=1&orderby=date&order=desc"
            r = requests.get(url, auth=(WP_USER, WP_APP_PASSWORD), timeout=15)
            r.raise_for_status()
            posts = r.json()
            if not posts:
                log.error("❌ Geen gepubliceerde posts gevonden")
                sys.exit(1)
            wp = posts[0]
            title = wp["title"]["rendered"]
            slug = wp["slug"]
            log.info(f"   📰 Gevonden: \"{title}\"")

        post_data = {
            "title": title,
            "slug": slug,
            "focus_keyword": "fitness",
        }
        try:
            linkedin_text = generate_linkedin_post(post_data)
            post_to_linkedin(linkedin_text)
            log.info("✅ LinkedIn post geplaatst!")
        except Exception as e:
            log.error(f"❌ LinkedIn fout: {e}", exc_info=True)
            sys.exit(1)
        return

    try:
        # Stap 0: Check topic queue
        log.info("📋 Stap 0: Topic queue checken...")
        queued_topic = pop_queued_topic()

        # Stap 1: Keywords ophalen
        keywords = fetch_trending_keywords()

        # Stap 2: Blogpost genereren (met queued topic als die er is)
        post_data = generate_blogpost(keywords, queued_topic=queued_topic)

        # Stap 3: Afbeelding genereren (optioneel)
        slug = post_data.get("slug", "blog-header")
        media_id = 0
        try:
            image_bytes = generate_image(post_data["dalle_prompt"])
            media_id = upload_image_to_wp(image_bytes, filename=f"{slug}.png")
        except Exception as img_err:
            log.warning(f"   ⚠️  Afbeelding overgeslagen: {img_err}")
            log.info("   ➡️  Post wordt zonder featured image gepubliceerd")

        # Stap 4: Post publiceren
        wp_post = create_wp_post(post_data, media_id)

        # LinkedIn wordt apart gepost via --linkedin-only op de publish-datum

        # Commit queue update als er een queued topic was
        if queued_topic:
            commit_queue_update()

        # Samenvatting
        log.info("")
        log.info("=" * 60)
        log.info("✅ KLAAR!")
        log.info(f"   Titel:      {post_data['title']}")
        log.info(f"   Keyword:    {post_data['focus_keyword']}")
        log.info(f"   Status:     Gepubliceerd")
        log.info(f"   Post ID:    {wp_post['id']}")
        log.info(f"   Link:       {wp_post.get('link', 'N/A')}")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"❌ Fout opgetreden: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
