#!/usr/bin/env python3
"""
Blog Automator voor seoprofessor.nl
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
WP_URL = os.getenv("WP_URL", "https://seoprofessor.nl")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

NL_TZ = ZoneInfo("Europe/Amsterdam")

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


# ── Stap 1: DataForSEO – Trending keywords ──────────────────────────
def fetch_trending_keywords():
    """Haal trending SEO-gerelateerde zoekwoorden op via DataForSEO."""
    log.info("📡 Stap 1: Trending keywords ophalen via DataForSEO...")

    url = "https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live"
    payload = [
        {
            "keyword": "SEO",
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
def _build_blogpost_prompt(keywords):
    """Bouw de prompt voor blogpost-generatie."""
    keyword_list = ", ".join(kw["keyword"] for kw in keywords[:5])

    today = datetime.now(NL_TZ).strftime("%d %B %Y")

    return f"""Je bent Stefan, een ervaren SEO-freelancer met 10+ jaar ervaring die schrijft voor seoprofessor.nl.
Vandaag is het {today}. Schrijf een diepgaande, waardevolle Nederlandse blogpost van MINIMAAL 1200 woorden over een trending SEO-onderwerp.

TRENDING KEYWORDS (kies het meest interessante onderwerp):
{keyword_list}

KWALITEITSEISEN:
- Dit moet een artikel zijn waar een SEO-professional daadwerkelijk iets van leert
- Geen oppervlakkige opsommingen — ga de diepte in met concrete voorbeelden, cijfers en praktijkcases
- Onderbouw claims met specifieke data, percentages of bronvermeldingen (bijv. "Uit onderzoek van Ahrefs blijkt...")
- Geef actionable tips die de lezer direct kan toepassen
- Beschrijf stap-voor-stap processen waar relevant
- Benoem veelgemaakte fouten en hoe je ze voorkomt
- Vergelijk tools, methodes of aanpakken waar dat relevant is

SCHRIJFSTIJL:
- Nederlandstalig, informeel maar professioneel (je/jij-vorm)
- Schrijf vanuit het perspectief van een SEO-expert die dagelijks met klanten werkt
- Natuurlijke, menselijke schrijfstijl — geen AI-achtige zinnen of clichés
- Varieer in zinslengte, gebruik af en toe spreektaal
- Deel persoonlijke ervaringen: "Bij een klant van mij zag ik laatst...", "In mijn ervaring..."
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
  "content": "De volledige HTML blogpost met <h2> subkoppen, <p> paragrafen, <ul>/<li> lijsten, eventueel <table> waar relevant. MINIMAAL 1200 woorden. Voeg ergens in de tekst deze link natuurlijk toe: <a href=\\"https://seoprofessor.nl/diensten\\">mijn SEO-diensten</a>. Gebruik GEEN <h1> tag (die komt van de titel).",
  "focus_keyword": "het hoofdkeyword van de post",
  "dalle_prompt": "Een Engelse prompt voor DALL-E om een professionele, moderne blogheader afbeelding te genereren die past bij het onderwerp. Stijl: clean, minimalistisch, digitaal marketing thema. Geen tekst in de afbeelding."
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


def generate_blogpost(keywords):
    """Genereer een Nederlandse blogpost. Probeert eerst Claude, fallback naar GPT-4o."""
    log.info("✍️  Stap 2: Blogpost genereren...")

    prompt = _build_blogpost_prompt(keywords)

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

    response = requests.post(
        url,
        headers=headers,
        data=image_bytes,
        auth=(WP_USER, WP_APP_PASSWORD),
        timeout=60,
    )
    response.raise_for_status()
    media = response.json()

    media_id = media["id"]
    media_url = media.get("source_url", "")

    log.info(f"   ✅ Afbeelding geüpload (ID: {media_id})")
    log.info(f"   🔗 URL: {media_url}")

    return media_id


# ── Stap 4b: WordPress – Post inplannen ─────────────────────────────
def create_wp_post(post_data, media_id, publish_date):
    """Maak een ingeplande WordPress post aan."""
    log.info("📝 Stap 4b: WordPress post aanmaken en inplannen...")

    # WordPress verwacht ISO 8601 in site-lokale tijd
    date_str = publish_date.strftime("%Y-%m-%dT%H:%M:%S")

    url = f"{WP_URL}/wp-json/wp/v2/posts"
    payload = {
        "title": post_data["title"],
        "content": post_data["content"],
        "status": "future",
        "date": date_str,
        "slug": post_data["slug"],
        "excerpt": post_data["meta_description"],
    }
    if media_id:
        payload["featured_media"] = media_id

    response = requests.post(
        url,
        json=payload,
        auth=(WP_USER, WP_APP_PASSWORD),
        timeout=30,
    )
    response.raise_for_status()
    wp_post = response.json()

    post_id = wp_post["id"]
    post_link = wp_post.get("link", "")

    log.info(f"   ✅ Post aangemaakt (ID: {post_id})")
    log.info(f"   🔗 Link: {post_link}")
    log.info(f"   📅 Ingepland: {date_str}")

    return wp_post


# ── Stap 5: LinkedIn – Post genereren en plaatsen ────────────────────
def get_linkedin_member_id():
    """Haal LinkedIn member ID (sub) op via userinfo endpoint."""
    response = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["sub"]


def generate_linkedin_post(post_data):
    """Genereer een LinkedIn post via Claude."""
    log.info("💬 Stap 5a: LinkedIn post genereren met Claude...")

    blog_url = f"https://seoprofessor.nl/{post_data['slug']}/"

    prompt = f"""Schrijf een pakkende LinkedIn post in het Nederlands.

BLOGPOST INFO:
- Titel: {post_data['title']}
- Onderwerp: {post_data['focus_keyword']}
- URL: {blog_url}

VEREISTEN:
- Max 1300 tekens (inclusief hashtags)
- Nederlandstalig
- Professioneel maar persoonlijk — schrijf als een SEO-freelancer die zijn kennis deelt
- Begin met een pakkende opening (hook) die aandacht trekt
- Vermeld de blogtitel en link naar het artikel
- Eindig met 3-5 relevante hashtags zoals #SEO #DigitalMarketing #SEOtips
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

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        json=payload,
        headers={
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        timeout=30,
    )
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
    log.info("🚀 Blog Automator voor seoprofessor.nl gestart")
    log.info("=" * 60)

    # Controleer environment variables
    missing = []
    for var in ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD", "ANTHROPIC_API_KEY",
                "OPENAI_API_KEY", "WP_USER", "WP_APP_PASSWORD",
                "LINKEDIN_ACCESS_TOKEN"]:
        if not os.getenv(var):
            missing.append(var)
    if missing:
        log.error(f"❌ Ontbrekende environment variabelen: {', '.join(missing)}")
        sys.exit(1)

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
            log.info("   Laatste ingeplande post ophalen van WordPress...")
            url = f"{WP_URL}/wp-json/wp/v2/posts?status=future&per_page=1&orderby=date&order=desc"
            r = requests.get(url, auth=(WP_USER, WP_APP_PASSWORD), timeout=15)
            r.raise_for_status()
            posts = r.json()
            if not posts:
                log.error("❌ Geen ingeplande posts gevonden")
                sys.exit(1)
            wp = posts[0]
            title = wp["title"]["rendered"]
            slug = wp["slug"]
            log.info(f"   📰 Gevonden: \"{title}\"")

        post_data = {
            "title": title,
            "slug": slug,
            "focus_keyword": "SEO",
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
        # Stap 1: Keywords ophalen
        keywords = fetch_trending_keywords()

        # Stap 2: Blogpost genereren
        post_data = generate_blogpost(keywords)

        # Stap 3: Afbeelding genereren (optioneel)
        slug = post_data.get("slug", "blog-header")
        media_id = 0
        try:
            image_bytes = generate_image(post_data["dalle_prompt"])
            media_id = upload_image_to_wp(image_bytes, filename=f"{slug}.png")
        except Exception as img_err:
            log.warning(f"   ⚠️  Afbeelding overgeslagen: {img_err}")
            log.info("   ➡️  Post wordt zonder featured image gepubliceerd")

        # Stap 4: Post inplannen
        publish_date = next_friday_9am()
        wp_post = create_wp_post(post_data, media_id, publish_date)

        # Stap 5: LinkedIn post
        try:
            linkedin_text = generate_linkedin_post(post_data)
            li_result = post_to_linkedin(linkedin_text)
        except Exception as li_err:
            log.warning(f"   ⚠️  LinkedIn overgeslagen: {li_err}")

        # Samenvatting
        log.info("")
        log.info("=" * 60)
        log.info("✅ KLAAR!")
        log.info(f"   Titel:      {post_data['title']}")
        log.info(f"   Keyword:    {post_data['focus_keyword']}")
        log.info(f"   Gepland:    {publish_date.strftime('%A %d %B %Y om %H:%M')} (NL-tijd)")
        log.info(f"   Post ID:    {wp_post['id']}")
        log.info(f"   Link:       {wp_post.get('link', 'N/A')}")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"❌ Fout opgetreden: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
