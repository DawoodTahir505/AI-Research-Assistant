import streamlit as st
from datetime import datetime

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="ResearchMind",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: #ffffff;
}

/* Main container */
.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #fafafa;
    border-right: 1px solid #eaeaea;
}

[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem;
}

/* Logo */
.logo {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: -0.6px;
    margin-bottom: 35px;
}

.logo-icon {
    display: inline-flex;
    width: 30px;
    height: 30px;
    align-items: center;
    justify-content: center;
    border-radius: 9px;
    background: #111111;
    color: white;
    margin-right: 8px;
}

/* Sidebar sections */
.sidebar-title {
    font-size: 12px;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: .8px;
    margin-bottom: 10px;
}

.pipeline-item {
    padding: 10px 0;
    font-size: 14px;
    color: #444;
    border-bottom: 1px solid #eeeeee;
}

.pipeline-number {
    color: #999;
    margin-right: 8px;
}

/* Hero */
.hero {
    text-align: center;
    padding: 75px 10px 30px 10px;
}

.hero h1 {
    font-size: 44px;
    font-weight: 700;
    letter-spacing: -2px;
    margin: 0;
    color: #111;
}

.hero p {
    margin-top: 14px;
    color: #777;
    font-size: 16px;
}

/* Input */
.input-label {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 7px;
    color: #333;
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #dddddd !important;
    background: #ffffff !important;
    font-size: 15px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #999999 !important;
    box-shadow: none !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    border-radius: 11px;
    height: 46px;
    font-weight: 600;
    border: none;
}

/* Normal buttons */
.stButton > button {
    border-radius: 10px;
}

/* Research header */
.result-header {
    margin-top: 35px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eeeeee;
}

.result-title {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -.8px;
    color: #111;
}

.muted {
    color: #888;
    font-size: 13px;
}

/* Report */
.report {
    margin-top: 18px;
    padding: 28px;
    border: 1px solid #e9e9e9;
    border-radius: 16px;
    background: #fff;
    line-height: 1.75;
}

/* Cards */
.metric-card {
    border: 1px solid #eeeeee;
    border-radius: 12px;
    padding: 15px;
    background: #fafafa;
    text-align: center;
}

.metric-number {
    font-size: 22px;
    font-weight: 700;
}

.metric-label {
    font-size: 12px;
    color: #888;
}

/* Expanders */
div[data-testid="stExpander"] {
    border: 1px solid #eeeeee;
    border-radius: 12px;
    margin-top: 10px;
}

/* Status */
div[data-testid="stStatus"] {
    border-radius: 12px;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #eeeeee;
    margin: 35px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "topic" not in st.session_state:
    st.session_state.topic = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="logo">
        <span class="logo-icon">✦</span>
        ResearchMind
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-title">Research Settings</div>',
        unsafe_allow_html=True
    )

    depth = st.selectbox(
        "Research depth",
        ["Standard", "Detailed", "Comprehensive"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-title">Pipeline</div>',
        unsafe_allow_html=True
    )

    pipeline = [
        ("01", "Web Search"),
        ("02", "Source Analysis"),
        ("03", "Report Writing"),
        ("04", "AI Review"),
    ]

    for number, name in pipeline:
        st.markdown(
            f"""
            <div class="pipeline-item">
                <span class="pipeline-number">{number}</span>
                {name}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="muted">Multi-agent research assistant</div>',
        unsafe_allow_html=True
    )


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<h1>What do you want to research?</h1>

<p>
Search the web. Analyze sources. Write a report. Review the results.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT AREA
# =========================================================

st.markdown(
    '<div class="input-label">Research topic</div>',
    unsafe_allow_html=True
)

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Impact of AI on healthcare in 2026",
    label_visibility="collapsed"
)

st.markdown(
    '<div class="input-label" style="margin-top:12px;">Additional context</div>',
    unsafe_allow_html=True
)

description = st.text_area(
    "Additional context",
    placeholder="Tell ResearchMind what you want to focus on... (optional)",
    height=90,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

run_btn = st.button(
    "✦  Start Research",
    type="primary",
    use_container_width=True
)


# =========================================================
# RESEARCH PIPELINE
# =========================================================

if run_btn:

    if not topic.strip():

        st.warning("Please enter a research topic.")

    else:

        st.session_state.results = {}
        st.session_state.topic = topic

        results = {}

        status = st.status(
            "ResearchMind is working...",
            expanded=True
        )

        try:

            # -------------------------------------------------
            # SEARCH
            # -------------------------------------------------

            status.write("🔎 Searching for reliable sources...")

            search_agent = build_search_agent()

            sr = search_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"""
                        Find recent and reliable information about:

                        {topic}

                        Additional context:
                        {description}

                        Research depth:
                        {depth}
                        """
                    )
                ]
            })

            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)


            # -------------------------------------------------
            # READER
            # -------------------------------------------------

            status.write("📖 Reading and analyzing sources...")

            reader_agent = build_reader_agent()

            rr = reader_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"""
                        Extract important and detailed information
                        about:

                        {topic}

                        Search results:
                        {results['search'][:5000]}
                        """
                    )
                ]
            })

            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)


            # -------------------------------------------------
            # WRITER
            # -------------------------------------------------

            status.write("✍️ Writing research report...")

            research_combined = (
                f"SEARCH RESULTS:\n"
                f"{results['search']}\n\n"
                f"SOURCE CONTENT:\n"
                f"{results['reader']}"
            )

            results["writer"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })

            st.session_state.results = dict(results)


            # -------------------------------------------------
            # CRITIC
            # -------------------------------------------------

            status.write("🧠 Reviewing report quality...")

            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })

            st.session_state.results = dict(results)

            status.update(
                label="Research completed",
                state="complete",
                expanded=False
            )

        except Exception as e:

            status.update(
                label="Research failed",
                state="error"
            )

            st.error(f"Error: {e}")


# =========================================================
# RESULTS
# =========================================================

r = st.session_state.results

if r:

    st.markdown("---")

    # -----------------------------------------------------
    # RESULT HEADER
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="result-header">
            <div class="result-title">
                {st.session_state.topic}
            </div>
            <div class="muted">
                Multi-agent research report
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">01</div>
            <div class="metric-label">Web Search</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">02</div>
            <div class="metric-label">Sources</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">03</div>
            <div class="metric-label">Report</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">04</div>
            <div class="metric-label">AI Review</div>
        </div>
        """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    if "writer" in r:

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### Research Report")

        st.markdown(
            f"""
            <div class="report">
                {r["writer"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "↓  Download Report",
                r["writer"],
                file_name=(
                    f"research_"
                    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                ),
                mime="text/markdown",
                use_container_width=True
            )

        with col2:

            if st.button(
                "Clear Research",
                use_container_width=True
            ):

                st.session_state.results = {}
                st.session_state.topic = ""

                st.rerun()


    # -----------------------------------------------------
    # RESEARCH PROCESS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown("### Research Process")

    if "search" in r:

        with st.expander("🔎  Web Search & Sources"):

            st.markdown(r["search"])


    if "reader" in r:

        with st.expander("📖  Source Analysis"):

            st.markdown(r["reader"])


    if "critic" in r:

        with st.expander("🧠  AI Critic Review"):

            st.markdown(r["critic"])


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
    text-align:center;
    color:#999;
    font-size:12px;
    margin-top:70px;
">
    ResearchMind · Multi-Agent AI Research Assistant
</div>
""", unsafe_allow_html=True)
