import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
from groq import Groq

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & ENTERPRISE DESIGN SYSTEM (CSS INJECTION)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Skylark Intelligence | Executive AI Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced High-End Dark UI & Glassmorphism Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        background-color: #05070E !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.08) 0px, transparent 50%);
        background-attachment: fixed;
        color: #F3F4F6;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* Executive Hero Header */
    .hero-card {
        background: rgba(13, 18, 30, 0.7);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 28px 36px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .hero-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .hero-subtitle {
        color: #9CA3AF;
        font-size: 14px;
        font-weight: 500;
        margin-top: 6px;
    }

    /* Live Pulse Badges */
    .badge-online {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }

    .badge-offline {
        background: rgba(239, 68, 68, 0.12);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: currentColor;
        box-shadow: 0 0 10px currentColor;
    }

    /* Glassmorphism Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }

    .glass-metric {
        background: rgba(15, 22, 38, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-top: 2px solid rgba(99, 102, 241, 0.6);
        border-radius: 16px;
        padding: 20px 24px;
        backdrop-filter: blur(16px);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .glass-metric:hover {
        transform: translateY(-4px);
        border-top-color: #818CF8;
        box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.3);
        background: rgba(20, 30, 50, 0.7);
    }

    .metric-label {
        color: #9CA3AF;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-val {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
        letter-spacing: -0.02em;
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(13, 18, 30, 0.8) !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 24px !important;
        color: #9CA3AF !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #080C16 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Button Styling */
    .stButton>button {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.03) !important;
        color: #E5E7EB !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        border-color: #6366F1 !important;
        background: rgba(99, 102, 241, 0.15) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MONDAY.COM & GROQ AI AGENT ENGINE
# -----------------------------------------------------------------------------
class SkylarkBIEngine:
    def __init__(self, monday_token, deals_board_id, work_orders_board_id, groq_api_key):
        self.monday_token = monday_token
        self.deals_board_id = deals_board_id
        self.work_orders_board_id = work_orders_board_id
        self.groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
        self.headers = {
            "Authorization": monday_token,
            "Content-Type": "application/json"
        }

    def fetch_board_data(self, board_id):
        if not self.monday_token or not board_id:
            return pd.DataFrame()
            
        query = f"""
        query {{
            boards (ids: {board_id}) {{
                name
                items_page (limit: 500) {{
                    items {{
                        name
                        column_values {{
                            column {{ title }}
                            text
                        }}
                    }}
                }}
            }}
        }}
        """
        try:
            res = requests.post(
                "https://api.monday.com/v2",
                json={"query": query},
                headers=self.headers,
                timeout=12
            )
            if res.status_code == 200:
                data = res.json()
                items = data['data']['boards'][0]['items_page']['items']
                
                rows = []
                for item in items:
                    row = {"Item Name": item['name']}
                    for cv in item['column_values']:
                        col_title = cv['column']['title']
                        row[col_title] = cv['text']
                    rows.append(row)
                return pd.DataFrame(rows)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching board {board_id}: {e}")
            return pd.DataFrame()

    def answer_query_stream(self, user_prompt, df_deals, df_wo):
        if not self.groq_client:
            yield "Groq API Key is missing. Please enter a valid API key in the sidebar."
            return

        deals_summary = df_deals.head(15).to_markdown(index=False) if not df_deals.empty else "No Deals Data"
        wo_summary = df_wo.head(15).to_markdown(index=False) if not df_wo.empty else "No Work Orders Data"

        system_prompt = f"""
        You are the Skylark Drones AI Executive Assistant. 
        Your task is to provide clear, actionable, executive-level business insights based on the provided data.

        Current Data Snapshots:
        
        ### Deals / Pipeline Board Snapshot:
        {deals_summary}

        ### Work Orders / Operations Board Snapshot:
        {wo_summary}

        Instructions:
        1. Keep answers structured using bullet points and markdown headers.
        2. Highlight key risks, operational bottlenecks, or notable revenue potential.
        3. Be precise and clear—avoid unnecessary fluff.
        """

        try:
            stream = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error generating insights: {e}"

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def get_grouping_column(df, preferred_keywords):
    if df.empty:
        return None
    cols = df.columns.tolist()
    for kw in preferred_keywords:
        for c in cols:
            if kw.lower() in c.lower():
                return c
    return cols[1] if len(cols) > 1 else cols[0]

# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/drone.png", width=48)
    st.markdown("<h3 style='color: #818CF8; margin: 0; font-weight: 800;'>SKYLARK HQ</h3>", unsafe_allow_html=True)
    st.caption("Telemetry Credentials & Pipeline Access")
    st.markdown("---")

    monday_token = st.text_input("Monday.com API Token", type="password")
    deals_board_id = st.text_input("Deals Board ID", value="5030217990")
    wo_board_id = st.text_input("Work Orders Board ID", value="5030217884")
    groq_api_key = st.text_input("Groq API Key (gsk_...)", type="password")

    st.markdown("<br>", unsafe_allow_html=True)
    connect_btn = st.button("🚀 Sync Workspace Engine", use_container_width=True)

# -----------------------------------------------------------------------------
# 5. DATA SYNC & SESSION STATE
# -----------------------------------------------------------------------------
if connect_btn:
    if not monday_token or not groq_api_key:
        st.sidebar.error("⚠️ Please enter both API keys to sync data.")
    else:
        engine = SkylarkBIEngine(monday_token, deals_board_id, wo_board_id, groq_api_key)
        with st.spinner("Establishing secure GraphQL handshake with Monday.com..."):
            st.session_state.df_deals = engine.fetch_board_data(deals_board_id)
            st.session_state.df_wo = engine.fetch_board_data(wo_board_id)
            st.session_state.engine = engine

df_deals = st.session_state.get("df_deals", pd.DataFrame())
df_wo = st.session_state.get("df_wo", pd.DataFrame())
engine = st.session_state.get("engine", None)

if "selected_preset" not in st.session_state:
    st.session_state.selected_preset = ""

# -----------------------------------------------------------------------------
# 6. EXECUTIVE HERO HUD
# -----------------------------------------------------------------------------
is_synced = not df_deals.empty

st.markdown(f"""
    <div class="hero-card">
        <div>
            <h1 class="hero-title">Executive Command Center</h1>
            <p class="hero-subtitle">Real-time Operations Telemetry & Automated Risk Intelligence</p>
        </div>
        <div>
            {"<div class='badge-online'><span class='pulse-dot'></span>SYSTEM SYNCED</div>" if is_synced else "<div class='badge-offline'><span class='pulse-dot'></span>DISCONNECTED</div>"}
        </div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. WORKSPACE TABS
# -----------------------------------------------------------------------------
tab1, tab2 = st.tabs(["🤖 AI Executive Assistant", "📊 Dynamic Telemetry Dashboard"])

# =============================================================================
# TAB 1: AI ASSISTANT WORKSPACE
# =============================================================================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### ⚡ Instant Executive Prompt Pills")
    q1, q2, q3 = st.columns(3)
    if q1.button("🚨 Detect Delayed Work Orders", use_container_width=True):
        st.session_state.selected_preset = "What are our top operational bottlenecks and delayed work orders?"
    if q2.button("💰 Summarize Pipeline Revenue", use_container_width=True):
        st.session_state.selected_preset = "Summarize total deal pipeline value and active revenue stages."
    if q3.button("📈 Field Operations Briefing", use_container_width=True):
        st.session_state.selected_preset = "Give me a high-level briefing on field team workload and work order distribution."

    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome back, Executive. I am synced with your Monday.com pipeline and ready for querying."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Query deal pipelines, work order delays, or team bottlenecks...")
    active_prompt = user_query or st.session_state.selected_preset

    if active_prompt:
        st.session_state.selected_preset = ""
        if not engine:
            st.error("⚠️ Please sync your workspace using sidebar credentials first.")
        else:
            st.session_state.messages.append({"role": "user", "content": active_prompt})
            with st.chat_message("user"):
                st.markdown(active_prompt)

            with st.chat_message("assistant"):
                response_generator = engine.answer_query_stream(active_prompt, df_deals, df_wo)
                full_response = st.write_stream(response_generator)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    if len(st.session_state.messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧹 Reset Conversation Context"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()

# =============================================================================
# TAB 2: TELEMETRY DASHBOARD
# =============================================================================
with tab2:
    if df_deals.empty and df_wo.empty:
        st.info("👋 Enter your API keys in the sidebar and click **'🚀 Sync Workspace Engine'** to populate live telemetry metrics.")
    else:
        # Compute Metrics
        total_val = 0
        val_col = next((c for c in df_deals.columns if any(k in c.lower() for k in ['value', 'amount', 'price', 'deal'])), None)
        if val_col and not df_deals.empty:
            cleaned_vals = pd.to_numeric(
                df_deals[val_col].astype(str).str.replace(r'[\$,]', '', regex=True),
                errors='coerce'
            ).fillna(0)
            total_val = cleaned_vals.sum()

        delayed_count = 0
        if not df_wo.empty:
            delayed_count = int(df_wo.astype(str).apply(
                lambda row: row.str.contains("delay|stuck|hold", case=False).any(), axis=1
            ).sum())

        # Bespoke Glass Cards Grid
        st.markdown(f"""
            <div class="metric-grid">
                <div class="glass-metric">
                    <div class="metric-label">Pipeline Deals</div>
                    <div class="metric-val">{len(df_deals)}</div>
                </div>
                <div class="glass-metric">
                    <div class="metric-label">Total Pipeline Value</div>
                    <div class="metric-val">${total_val:,.2f}</div>
                </div>
                <div class="glass-metric">
                    <div class="metric-label">Active Work Orders</div>
                    <div class="metric-val">{len(df_wo)}</div>
                </div>
                <div class="glass-metric" style="border-top-color: {"#EF4444" if delayed_count > 0 else "#10B981"};">
                    <div class="metric-label">Flagged Delay Risks</div>
                    <div class="metric-val" style="color: {"#F87171" if delayed_count > 0 else "#34D399"};">{delayed_count}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if delayed_count > 0:
            st.warning(f"🚨 **Operational Risk Detected**: {delayed_count} Work Orders are flagged with field delays or holds.")
        else:
            st.success("✅ **Operations Normal**: Field telemetry indicates zero delayed projects.")

        st.markdown("---")

        # Filters Section
        st.markdown("##### 🔍 Real-Time Dataset Filters")
        f1, f2 = st.columns(2)
        with f1:
            deals_filter = st.text_input("Filter Deals (e.g. Solar, Open, Won):", value="")
        with f2:
            wo_filter = st.text_input("Filter Work Orders (e.g. Delayed, Maintenance):", value="")

        filtered_deals = df_deals.copy()
        if deals_filter and not filtered_deals.empty:
            filtered_deals = filtered_deals[filtered_deals.astype(str).apply(lambda r: r.str.contains(deals_filter, case=False, na=False).any(), axis=1)]

        filtered_wo = df_wo.copy()
        if wo_filter and not filtered_wo.empty:
            filtered_wo = filtered_wo[filtered_wo.astype(str).apply(lambda r: r.str.contains(wo_filter, case=False, na=False).any(), axis=1)]

        st.markdown("<br>", unsafe_allow_html=True)
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("#### 💼 Deals Distribution")
            if not filtered_deals.empty:
                g_col_deals = get_grouping_column(filtered_deals, ["status", "stage", "owner", "type"])
                d_counts = filtered_deals[g_col_deals].value_counts().reset_index()
                d_counts.columns = [g_col_deals, "Count"]

                fig_deals = px.bar(
                    d_counts, x=g_col_deals, y="Count", text="Count",
                    color="Count",
                    color_continuous_scale=["#6366F1", "#A855F7", "#EC4899"]
                )
                fig_deals.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=360,
                    margin=dict(l=10, r=10, t=30, b=10)
                )
                st.plotly_chart(fig_deals, use_container_width=True)

        with chart_col2:
            st.markdown("#### 🛠️ Work Orders Breakdown")
            if not filtered_wo.empty:
                g_col_wo = get_grouping_column(filtered_wo, ["status", "stage", "state", "owner"])
                w_counts = filtered_wo[g_col_wo].value_counts().reset_index()
                w_counts.columns = [g_col_wo, "Count"]

                fig_wo = px.bar(
                    w_counts, x=g_col_wo, y="Count", text="Count",
                    color="Count",
                    color_continuous_scale=["#3B82F6", "#06B6D4", "#10B981"]
                )
                fig_wo.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=360,
                    margin=dict(l=10, r=10, t=30, b=10)
                )
                st.plotly_chart(fig_wo, use_container_width=True)

        st.markdown("---")

        d_tab1, d_tab2 = st.columns(2)
        with d_tab1:
            st.markdown("##### Deals Dataset Snapshot")
            st.dataframe(filtered_deals, use_container_width=True, height=260)
            if not filtered_deals.empty:
                st.download_button("📥 Export Deals CSV", data=filtered_deals.to_csv(index=False), file_name="skylark_deals.csv", mime="text/csv", use_container_width=True)

        with d_tab2:
            st.markdown("##### Work Orders Dataset Snapshot")
            st.dataframe(filtered_wo, use_container_width=True, height=260)
            if not filtered_wo.empty:
                st.download_button("📥 Export Work Orders CSV", data=filtered_wo.to_csv(index=False), file_name="skylark_work_orders.csv", mime="text/csv", use_container_width=True)