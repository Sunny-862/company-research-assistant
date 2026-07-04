import re
from urllib.parse import urlparse

import streamlit as st

from services.serper_service import (
    find_official_website,
    research_company_search,
)
from services.crawler import crawl_website
from services.openrouter_service import analyze_company
from services.competitor_service import find_competitors
from services.pdf_service import generate_company_report
from utils.helpers import (
    is_valid_url,
    normalize_website_url,
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Research AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# HTML HELPER
# ==================================================

def render_html(html):
    """
    Safely render multiline HTML without Streamlit
    interpreting indentation as Markdown code blocks.
    """
    lines = html.strip("\n").split("\n")
    cleaned_html = "\n".join(line.strip() for line in lines)

    st.markdown(
        cleaned_html,
        unsafe_allow_html=True,
    )


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg:        #0a0b0c;
    --panel:     #121417;
    --panel-2:   #15181c;
    --line:      #23262c;
    --line-soft: #1a1d22;
    --text:      #eef0f2;
    --fog:       #868c96;
    --fog-dim:   #565b64;
    --signal:    #35e0c1;
    --signal-soft: rgba(53, 224, 193, 0.10);
    --signal-line: rgba(53, 224, 193, 0.30);
    --ember:     #ff7a52;
    --ember-soft: rgba(255, 122, 82, 0.10);
    --ember-line: rgba(255, 122, 82, 0.28);
    --font-display: 'Space Grotesk', 'IBM Plex Sans', sans-serif;
    --font-body:    'IBM Plex Sans', -apple-system, sans-serif;
    --font-mono:    'IBM Plex Mono', 'Courier New', monospace;
}

* {
    font-family: var(--font-body);
}

.stApp {
    background:
        radial-gradient(circle at 12% -6%, rgba(53, 224, 193, 0.07), transparent 42%),
        radial-gradient(circle at 88% 4%, rgba(255, 122, 82, 0.045), transparent 46%),
        radial-gradient(rgba(255, 255, 255, 0.022) 1px, transparent 1px),
        var(--bg);
    background-size: auto, auto, 24px 24px, auto;
}

.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 8rem;
    position: relative;
}

.block-container::before {
    content: "";
    position: fixed;
    inset: -10%;
    z-index: -1;
    pointer-events: none;
    background:
        radial-gradient(560px circle at 18% 8%, var(--signal-soft), transparent 60%),
        radial-gradient(460px circle at 92% 18%, var(--ember-soft), transparent 58%);
    animation: driftGlow 24s ease-in-out infinite alternate;
}

@keyframes driftGlow {
    0%   { transform: translate(0%, 0%); opacity: 0.85; }
    100% { transform: translate(-2%, 2.5%); opacity: 1; }
}

header[data-testid="stHeader"] {
    background: rgba(10, 11, 12, 0);
}

#MainMenu, footer {
    visibility: hidden;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0d0f12;
    border-right: 1px solid var(--line-soft);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
}

.sidebar-brand {
    padding: 0.2rem 0 1.4rem 0;
    border-bottom: 1px solid var(--line-soft);
    margin-bottom: 1.6rem;
}

.sidebar-brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
}

.sidebar-logo {
    position: relative;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(150deg, #1a2a28, #0f1214);
    border: 1px solid var(--line);
    color: var(--signal);
    font-family: var(--font-display);
    font-size: 18px;
    font-weight: 700;
}

.sidebar-logo::before {
    content: "";
    position: absolute;
    inset: -4px;
    border-radius: 13px;
    padding: 1px;
    background: conic-gradient(from 0deg, transparent 0%, var(--signal) 12%, transparent 26%, transparent 100%);
    -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    animation: ringSpin 5.5s linear infinite;
}

@keyframes ringSpin {
    to { transform: rotate(360deg); }
}

.sidebar-title {
    color: var(--text);
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.2px;
}

.sidebar-subtitle {
    color: var(--fog-dim);
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.8px;
    margin-top: 3px;
}

.sidebar-section-label {
    color: var(--fog-dim);
    font-family: var(--font-mono);
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 1.6px;
    margin-top: 1.6rem;
    margin-bottom: 0.7rem;
}

.sidebar-info-title {
    color: var(--text);
    font-family: var(--font-display);
    font-size: 12.5px;
    font-weight: 700;
    margin-bottom: 14px;
}

.sidebar-info {
    background: linear-gradient(165deg, var(--panel-2), #0e1013);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 18px;
    margin-top: 1.2rem;
}

.how-it-works-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    color: var(--fog);
    font-size: 12px;
    line-height: 1.5;
}

.how-it-works-num {
    flex-shrink: 0;
    width: 22px;
    height: 20px;
    border-radius: 5px;
    background: transparent;
    border: 1px solid var(--line);
    color: var(--signal);
    font-family: var(--font-mono);
    font-size: 9.5px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
}

.tech-footer {
    color: var(--fog-dim);
    font-family: var(--font-mono);
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 1.5px;
    margin-top: 2.2rem;
    padding-top: 1.1rem;
    border-top: 1px solid var(--line-soft);
}


/* HERO */

.hero-wrapper {
    text-align: center;
    padding-top: 8vh;
    padding-bottom: 3rem;
}

.hero-eyebrow {
    display: inline-block;
    color: var(--signal);
    background: var(--signal-soft);
    border: 1px solid var(--signal-line);
    border-radius: 20px;
    padding: 6px 16px;
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2.4px;
    margin-bottom: 26px;
}

.hero-title {
    color: var(--text);
    font-family: var(--font-display);
    font-size: clamp(42px, 5.2vw, 68px);
    font-weight: 700;
    line-height: 1.08;
    letter-spacing: -2.2px;
    margin-bottom: 22px;
}

.hero-title-accent {
    position: relative;
    display: inline-block;
    background: linear-gradient(135deg, var(--signal), #1fa88f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-title-accent::after {
    content: "";
    position: absolute;
    left: 2px;
    right: 2px;
    bottom: -4px;
    height: 2px;
    border-radius: 2px;
    background: linear-gradient(90deg, transparent, var(--signal) 45%, var(--ember) 55%, transparent);
    background-size: 220% 100%;
    animation: scanline 4s ease-in-out infinite;
}

@keyframes scanline {
    0%   { background-position: 0% 0%; opacity: 0.5; }
    50%  { background-position: 100% 0%; opacity: 1; }
    100% { background-position: 0% 0%; opacity: 0.5; }
}

.hero-subtitle {
    color: var(--fog);
    font-size: 15.5px;
    line-height: 1.75;
    max-width: 600px;
    margin: 0 auto;
}

.example-row {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 14px;
}

.example-chip {
    display: inline-block;
    background: var(--panel);
    border: 1px solid var(--line);
    color: var(--fog);
    border-radius: 8px;
    padding: 8px 18px;
    margin: 4px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.example-chip:hover {
    border-color: var(--signal-line);
    color: var(--text);
    transform: translateY(-2px);
}

.hero-hint {
    color: var(--fog-dim);
    text-align: center;
    font-family: var(--font-mono);
    font-size: 9.5px;
    font-weight: 500;
    letter-spacing: 1.4px;
    margin-top: 22px;
}


/* SECTION HEADER */

.section-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}

.section-heading-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title {
    color: var(--text);
    font-family: var(--font-display);
    font-size: 15px;
    font-weight: 700;
}

.live-badge {
    position: relative;
    background: var(--signal-soft);
    border: 1px solid var(--signal-line);
    color: var(--signal);
    font-family: var(--font-mono);
    font-size: 8.5px;
    font-weight: 600;
    letter-spacing: 1.2px;
    padding: 4px 10px 4px 17px;
    border-radius: 10px;
}

.live-badge::before {
    content: "";
    position: absolute;
    left: 8px;
    top: 50%;
    width: 5px;
    height: 5px;
    margin-top: -2.5px;
    border-radius: 50%;
    background: var(--signal);
    box-shadow: 0 0 6px var(--signal);
    animation: pulseDot 1.8s ease-in-out infinite;
}

@keyframes pulseDot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.4; transform: scale(0.65); }
}


/* COMPANY HEADER */

.company-header {
    background: linear-gradient(150deg, var(--panel-2) 0%, #0d0f13 100%);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 28px 30px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.company-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    color: #4bc98a;
    font-family: var(--font-mono);
    font-size: 9.5px;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 12px;
}

.company-status::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4bc98a;
    box-shadow: 0 0 8px #4bc98a;
    animation: pulseDot 2.2s ease-in-out infinite;
}

.company-name {
    color: var(--text);
    font-family: var(--font-display);
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 8px;
}

.company-url {
    color: var(--signal);
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 500;
    word-break: break-all;
}


/* INFORMATION CARDS */

.info-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 18px 20px;
    min-height: 92px;
    margin-bottom: 12px;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

.info-card:hover {
    transform: perspective(700px) rotateX(2deg) translateY(-3px);
    border-color: var(--signal-line);
    box-shadow: 0 14px 28px rgba(0, 0, 0, 0.35);
}

.info-label {
    color: var(--fog-dim);
    font-family: var(--font-mono);
    font-size: 8.5px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.info-value {
    color: var(--text);
    font-size: 12.5px;
    font-weight: 500;
    line-height: 1.6;
    word-break: break-word;
}


/* CONTENT */

.content-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 13px;
    padding: 24px;
    margin-top: 16px;
    margin-bottom: 16px;
    transition: border-color 0.25s ease;
}

.content-card:hover {
    border-color: var(--line);
}

.content-title {
    color: var(--signal);
    font-family: var(--font-mono);
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.summary-text {
    color: var(--fog);
    font-size: 13.5px;
    line-height: 1.85;
}


/* PRODUCTS */

.product-chip {
    display: inline-block;
    color: var(--text);
    background: var(--panel-2);
    border: 1px solid var(--line);
    border-radius: 7px;
    padding: 8px 13px;
    margin: 4px 6px 4px 0;
    font-size: 11.5px;
    font-weight: 500;
    transition: border-color 0.2s ease, transform 0.2s ease;
}

.product-chip:hover {
    border-color: var(--signal-line);
    transform: translateY(-1px);
}


/* PAIN POINTS */

.pain-point {
    color: var(--fog);
    background: var(--panel-2);
    border-left: 3px solid var(--ember);
    padding: 12px 16px;
    margin-bottom: 10px;
    border-radius: 0 8px 8px 0;
    font-size: 12.5px;
    line-height: 1.65;
}


/* COMPETITORS */

.competitor-card {
    background: var(--panel-2);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 15px 17px;
    margin-bottom: 10px;
    transition: transform 0.25s ease, border-color 0.25s ease;
}

.competitor-card:hover {
    transform: perspective(700px) rotateX(1.5deg) translateY(-2px);
    border-color: var(--signal-line);
}

.competitor-name {
    color: var(--text);
    font-size: 12.5px;
    font-weight: 650;
    margin-bottom: 5px;
}

.competitor-url {
    color: var(--signal);
    font-family: var(--font-mono);
    font-size: 10.5px;
    word-break: break-all;
}

.disclaimer {
    color: var(--fog-dim);
    font-size: 10.5px;
    line-height: 1.65;
    margin-top: 14px;
}


/* BUTTON */

.stDownloadButton button {
    background: linear-gradient(135deg, #45f0cf, #1fa88f) !important;
    color: #06120f !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
    min-height: 46px;
    box-shadow: 0 6px 18px rgba(53, 224, 193, 0.2);
    transition: all 0.2s ease !important;
}

.stDownloadButton button:hover {
    background: linear-gradient(135deg, #5cf5d7, #27bda2) !important;
    box-shadow: 0 8px 22px rgba(53, 224, 193, 0.32);
    transform: translateY(-1px);
}


/* CHAT INPUT */

div[data-testid="stChatInput"] {
    border: 1px solid var(--line);
    background: var(--panel);
    border-radius: 12px;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: var(--signal);
    box-shadow: 0 0 0 3px var(--signal-soft);
}


/* SELECTBOX */

div[data-testid="stSelectbox"] > div {
    background: var(--panel);
    border-radius: 9px;
}


/* STATUS */

div[data-testid="stStatusWidget"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
}


/* EXPANDERS */

div[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 11px;
}


@media (prefers-reduced-motion: reduce) {

    .block-container::before,
    .sidebar-logo::before,
    .hero-title-accent::after,
    .live-badge::before,
    .company-status::before {
        animation: none !important;
    }
}


@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero-wrapper {
        padding-top: 4vh;
    }

    .hero-title {
        font-size: 40px;
    }

    .company-name {
        font-size: 25px;
    }
}
</style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# INPUT VALIDATION
# ==================================================

def validate_company_input(user_input):

    if not user_input or not user_input.strip():
        return False, "Please enter a company name or website URL."

    cleaned_input = user_input.strip()

    if "\n" in cleaned_input or "\r" in cleaned_input:
        return False, "Please research only one company at a time."

    if len(cleaned_input) > 200:
        return (
            False,
            "Input is too long. Please enter a valid company name or website URL.",
        )

    if cleaned_input.startswith(("http://", "https://")):

        parsed_url = urlparse(cleaned_input)

        if not parsed_url.netloc or "." not in parsed_url.netloc:
            return False, "Please enter a valid website URL."

    return True, cleaned_input


# ==================================================
# SESSION STATE
# ==================================================

session_defaults = {
    "research_result": None,
    "competitors": None,
    "search_results": [],
    "crawled_pages": [],
}

for key, default_value in session_defaults.items():

    if key not in st.session_state:
        st.session_state[key] = default_value


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-row">

                <div class="sidebar-logo">
                    R
                </div>

                <div>
                    <div class="sidebar-title">
                        Research AI
                    </div>

                    <div class="sidebar-subtitle">
                        COMPANY INTELLIGENCE
                    </div>
                </div>

            </div>
        </div>
        """
    )

    render_html(
        """
        <div class="sidebar-section-label">
            RESEARCH CONFIGURATION
        </div>
        """
    )

    selected_model = st.selectbox(
        "AI Model",
        [
            "openai/gpt-4o-mini",
            "google/gemini-2.0-flash-001",
            "anthropic/claude-3.5-haiku",
        ],
    )

    render_html(
        """
        <div class="sidebar-info">

            <div class="sidebar-info-title">
                How it works
            </div>

            <div class="how-it-works-row">
                <div class="how-it-works-num">1</div>
                <div>Enter a company or URL</div>
            </div>

            <div class="how-it-works-row">
                <div class="how-it-works-num">2</div>
                <div>Discover and crawl website</div>
            </div>

            <div class="how-it-works-row">
                <div class="how-it-works-num">3</div>
                <div>Collect public research</div>
            </div>

            <div class="how-it-works-row">
                <div class="how-it-works-num">4</div>
                <div>Generate AI intelligence</div>
            </div>

            <div class="how-it-works-row">
                <div class="how-it-works-num">5</div>
                <div>Identify competitors</div>
            </div>

            <div class="how-it-works-row">
                <div class="how-it-works-num">6</div>
                <div>Download professional PDF</div>
            </div>

        </div>

        <div class="tech-footer">
            OPENROUTER · SERPER · PYTHON
        </div>
        """
    )


# ==================================================
# SESSION RESULTS
# ==================================================

analysis = st.session_state.research_result
competitors = st.session_state.competitors
search_results = st.session_state.search_results
crawled_pages = st.session_state.crawled_pages


# ==================================================
# LANDING PAGE
# ==================================================

if not analysis:

    render_html(
        """
        <div class="hero-wrapper">

            <div class="hero-eyebrow">
                AI-POWERED COMPANY INTELLIGENCE
            </div>

            <div class="hero-title">
                Know any company<br>
                <span class="hero-title-accent">in minutes.</span>
            </div>

            <div class="hero-subtitle">
                Enter a company name or website URL to get
                AI-powered insights, company intelligence,
                competitor analysis, business pain points,
                and a professional research report.
            </div>

            <div class="example-row">
                <span class="example-chip">Microsoft</span>
                <span class="example-chip">Stripe</span>
                <span class="example-chip">Tesla</span>
                <span class="example-chip">NVIDIA</span>
            </div>

            <div class="hero-hint">
                ENTER TO RESEARCH · POWERED BY LIVE WEB INTELLIGENCE
            </div>

        </div>
        """
    )

else:

    render_html(
        """
        <div class="section-heading">

            <div class="section-heading-left">

                <div class="section-title">
                    Company Research
                </div>

                <div class="live-badge">
                    LIVE
                </div>

            </div>

        </div>
        """
    )


# ==================================================
# CHAT INPUT
# ==================================================

company_input = st.chat_input(
    "Enter a company name or website URL..."
)


# ==================================================
# RESEARCH PIPELINE
# ==================================================

# ==================================================
# RESEARCH PIPELINE
# ==================================================

if company_input:

    is_valid, validation_result = validate_company_input(
        company_input
    )

    if not is_valid:

        st.error(validation_result)

    else:

        company_input = validation_result

        # Clear previous research results
        st.session_state.research_result = None
        st.session_state.competitors = None
        st.session_state.search_results = []
        st.session_state.crawled_pages = []

        with st.chat_message("user"):
            st.write(company_input)

        with st.chat_message("assistant"):

            status = st.status(
                "Starting company intelligence research...",
                expanded=True,
            )

            try:

                # ==========================================
                # STEP 1: ANALYZE INPUT
                # ==========================================

                status.write(
                    "🔎 Analyzing company input..."
                )

                if is_valid_url(company_input):

                    website = normalize_website_url(
                        company_input
                    )

                    research_query = website

                    status.write(
                        "✓ Website URL detected."
                    )

                else:

                    # ======================================
                    # STEP 2: FIND OFFICIAL WEBSITE
                    # ======================================

                    status.write(
                        "🌐 Discovering official company website..."
                    )

                    website = find_official_website(
                        company_input
                    )

                    if not website:

                        raise RuntimeError(
                            "Unable to identify a reliable "
                            "official company website."
                        )

                    research_query = company_input

                    status.write(
                        f"✓ Official website identified: {website}"
                    )


                # ==========================================
                # STEP 3: CRAWL WEBSITE
                # ==========================================

                status.write(
                    "🕸️ Crawling important company pages..."
                )

                try:

                    crawled_pages = crawl_website(
                        website
                    )

                    if crawled_pages:

                        status.write(
                            f"✓ Analyzed "
                            f"{len(crawled_pages)} "
                            f"company pages."
                        )

                    else:

                        status.write(
                            "⚠️ No website pages could be "
                            "crawled. Continuing with public "
                            "web intelligence..."
                        )

                except Exception:

                    # IMPORTANT:
                    # Some websites such as Nike may block
                    # automated crawling.
                    #
                    # The application should NOT fail because
                    # public search results can still be used.

                    crawled_pages = []

                    status.write(
                        "⚠️ Website crawling was restricted. "
                        "Continuing with public web intelligence..."
                    )


                # ==========================================
                # STEP 4: PUBLIC WEB RESEARCH
                # ==========================================

                status.write(
                    "🔍 Collecting public web intelligence..."
                )

                try:

                    search_results = research_company_search(
                        research_query
                    )

                except Exception:

                    search_results = []

                    status.write(
                        "⚠️ Some public web research requests "
                        "were unavailable."
                    )


                if search_results:

                    status.write(
                        f"✓ Collected "
                        f"{len(search_results)} "
                        f"public sources."
                    )

                else:

                    status.write(
                        "⚠️ No additional public web sources "
                        "were collected."
                    )


                # ==========================================
                # STEP 5: CHECK AVAILABLE DATA
                # ==========================================

                if not crawled_pages and not search_results:

                    raise RuntimeError(
                        "No reliable company information "
                        "could be collected from the company "
                        "website or public web sources."
                    )


                # ==========================================
                # STEP 6: AI COMPANY ANALYSIS
                # ==========================================

                status.write(
                    "🤖 Generating AI-powered "
                    "company intelligence..."
                )

                analysis = analyze_company(
                    company_name=research_query,
                    website=website,
                    crawled_pages=crawled_pages,
                    search_results=search_results,
                    model=selected_model,
                )

                if not analysis:

                    raise RuntimeError(
                        "AI analysis did not return "
                        "a valid result."
                    )

                status.write(
                    "✓ AI company analysis completed."
                )


                # ==========================================
                # STEP 7: COMPETITOR RESEARCH
                # ==========================================

                status.write(
                    "🏢 Discovering and validating "
                    "competitors..."
                )

                try:

                    competitors = find_competitors(
                        company_name=analysis.get(
                            "company_name",
                            research_query,
                        ),
                        company_website=analysis.get(
                            "website",
                            website,
                        ),
                        industry=analysis.get(
                            "industry",
                            "Not available",
                        ),
                        country=analysis.get(
                            "country",
                            "Not available",
                        ),
                        products_services=analysis.get(
                            "products_services",
                            [],
                        ),
                        model=selected_model,
                    )

                    if competitors is None:
                        competitors = []

                    status.write(
                        f"✓ Identified "
                        f"{len(competitors)} "
                        f"relevant competitors."
                    )

                except Exception:

                    # Competitor failure should also not
                    # destroy the complete company research.

                    competitors = []

                    status.write(
                        "⚠️ Competitor research was unavailable. "
                        "Continuing with company results..."
                    )


                # ==========================================
                # STEP 8: SAVE SESSION RESULTS
                # ==========================================

                st.session_state.research_result = analysis
                st.session_state.competitors = competitors
                st.session_state.search_results = search_results
                st.session_state.crawled_pages = crawled_pages


                # ==========================================
                # STEP 9: COMPLETE
                # ==========================================

                status.update(
                    label="Research completed successfully",                
                    expanded=False,
                )

                st.rerun()


            except Exception as error:

                status.update(
                    label="Research failed",
                    state="error",
                )

                st.error(
                    f"Unable to complete research: {error}"
                )

# ==================================================
# REFRESH RESULTS
# ==================================================

analysis = st.session_state.research_result
competitors = st.session_state.competitors
search_results = st.session_state.search_results
crawled_pages = st.session_state.crawled_pages


# ==================================================
# DISPLAY RESULTS
# ==================================================

if analysis:

    company_name = analysis.get(
        "company_name",
        "Company",
    )

    website = analysis.get(
        "website",
        "Not available",
    )

    industry = analysis.get(
        "industry",
        "Not available",
    )

    country = analysis.get(
        "country",
        "Not available",
    )

    phone = analysis.get(
        "phone_number",
        "Not available",
    )

    address = analysis.get(
        "address",
        "Not available",
    )


    # COMPANY HEADER

    render_html(
        f"""
        <div class="company-header">

            <div class="company-status">
                RESEARCH COMPLETE
            </div>

            <div class="company-name">
                {company_name}
            </div>

            <div class="company-url">
                {website}
            </div>

        </div>
        """
    )


    # INFORMATION CARDS

    col1, col2, col3 = st.columns(3)

    with col1:

        render_html(
            f"""
            <div class="info-card">

                <div class="info-label">
                    Industry
                </div>

                <div class="info-value">
                    {industry}
                </div>

            </div>
            """
        )

    with col2:

        render_html(
            f"""
            <div class="info-card">

                <div class="info-label">
                    Country
                </div>

                <div class="info-value">
                    {country}
                </div>

            </div>
            """
        )

    with col3:

        render_html(
            f"""
            <div class="info-card">

                <div class="info-label">
                    Phone
                </div>

                <div class="info-value">
                    {phone}
                </div>

            </div>
            """
        )


    render_html(
        f"""
        <div class="info-card">

            <div class="info-label">
                Address
            </div>

            <div class="info-value">
                {address}
            </div>

        </div>
        """
    )


    # COMPANY SUMMARY

    summary = analysis.get(
        "company_summary",
        "No company summary available.",
    )

    render_html(
        f"""
        <div class="content-card">

            <div class="content-title">
                Company Intelligence Summary
            </div>

            <div class="summary-text">
                {summary}
            </div>

        </div>
        """
    )


    # PRODUCTS

    products = analysis.get(
        "products_services",
        [],
    )

    product_html = ""

    for product in products:

        product_html += (
            f'<span class="product-chip">'
            f'{product}'
            f'</span>'
        )

    if not product_html:

        product_html = (
            '<div class="summary-text">'
            'No products or services identified.'
            '</div>'
        )

    render_html(
        f"""
        <div class="content-card">

            <div class="content-title">
                Products & Services
            </div>

            {product_html}

        </div>
        """
    )


    # PAIN POINTS

    pain_points = analysis.get(
        "pain_points",
        [],
    )

    pain_html = ""

    for pain_point in pain_points:

        pain_html += (
            f'<div class="pain-point">'
            f'{pain_point}'
            f'</div>'
        )

    if not pain_html:

        pain_html = (
            '<div class="summary-text">'
            'No AI-generated pain points available.'
            '</div>'
        )

    render_html(
        f"""
        <div class="content-card">

            <div class="content-title">
                AI-Generated Business Pain Points
            </div>

            {pain_html}

            <div class="disclaimer">
                AI-generated inferences based on collected
                company, website, and industry information.
            </div>

        </div>
        """
    )


    # COMPETITORS

    competitor_html = ""

    if competitors:

        for competitor in competitors:

            competitor_name = competitor.get(
                "company_name",
                "Competitor",
            )

            competitor_website = competitor.get(
                "website",
                "Not available",
            )

            competitor_html += f"""
            <div class="competitor-card">

                <div class="competitor-name">
                    {competitor_name}
                </div>

                <div class="competitor-url">
                    {competitor_website}
                </div>

            </div>
            """

    else:

        competitor_html = (
            '<div class="summary-text">'
            'No validated competitors identified.'
            '</div>'
        )

    render_html(
        f"""
        <div class="content-card">

            <div class="content-title">
                Competitive Landscape
            </div>

            {competitor_html}

        </div>
        """
    )


    # RESEARCH SOURCES

    with st.expander(
        "🔗 View Research Sources",
        expanded=False,
    ):

        source_urls = set()

        if crawled_pages:

            st.markdown(
                "#### Company Website Pages"
            )

            for page in crawled_pages:

                page_url = page.get(
                    "url",
                    "",
                )

                if (
                    page_url
                    and page_url not in source_urls
                ):

                    source_urls.add(
                        page_url
                    )

                    st.markdown(
                        f"- [{page_url}]({page_url})"
                    )

        if search_results:

            st.markdown(
                "#### Public Web Sources"
            )

            displayed_sources = 0

            for result in search_results:

                title = result.get(
                    "title",
                    "Research Source",
                )

                link = result.get(
                    "link",
                    "",
                )

                if (
                    link
                    and link not in source_urls
                ):

                    source_urls.add(
                        link
                    )

                    st.markdown(
                        f"- [{title}]({link})"
                    )

                    displayed_sources += 1

                if displayed_sources >= 10:
                    break

        if not source_urls:

            st.info(
                "No research sources available."
            )


    # PDF

    render_html(
        """
        <div style="
            margin-top: 22px;
            margin-bottom: 12px;
            color: #d3a84f;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1.6px;
        ">
            PROFESSIONAL RESEARCH REPORT
        </div>
        """
    )

    try:

        pdf_bytes = generate_company_report(
            analysis=analysis,
            competitors=competitors or [],
            search_results=search_results,
            crawled_pages=crawled_pages,
        )

        safe_company_name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            company_name,
        ).strip("_").lower()

        st.download_button(
            label="↓  Download PDF Research Report",
            data=pdf_bytes,
            file_name=f"{safe_company_name}_research_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as error:

        st.error(
            f"Unable to generate PDF report: {error}"
        )