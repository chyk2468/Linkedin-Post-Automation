import streamlit as st
import datetime
import pandas as pd
import json
import os
from pathlib import Path
from core.automation import AutomationPipeline
from config.config import DAY_TOPICS, LOGS_DIR, DATA_DIR, OUTPUT_DIR
from core.logger import get_last_post_date, delete_post

# Page Config
st.set_page_config(
    page_title="LinkedIn AI Poster Pro", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "SaaS Dashboard" look
st.markdown("""
<style>
    /* Card Styling */
    .st-emotion-cache-12w0qpk {
        border: 1px solid #2970FF;
        border-radius: 10px;
        padding: 20px;
        background-color: #1E2130;
    }
    
    /* Title and Header styling */
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(90deg, #2970FF, #00E676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem !important;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #2970FF;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-image: linear-gradient(#0E1117,#0E1117);
        color: white;
    }
    
    /* Button Hover */
    .stButton>button:hover {
        border-color: #00E676;
        color: #00E676;
    }
</style>
""", unsafe_allow_html=True)

# Helper for history loading
def load_history():
    history_file = DATA_DIR / "post_log.jsonl"
    if history_file.exists():
        with open(history_file, 'r') as f:
            return [json.loads(line) for line in f.readlines()]
    return []

# App Header
st.title("🚀 LinkedIn AI Auto-Poster Pro")

# --- TOP KPI BAR ---
history_data = load_history()
last_post = get_last_post_date()
today_name = datetime.datetime.now().strftime("%A")
today_topic = DAY_TOPICS[datetime.datetime.now().weekday()]['name']

m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Day", today_name)
m2.metric("Today's Focus", today_topic)
m3.metric("Total Posts", len(history_data))
m4.metric("Last Activity", str(last_post) if last_post else "N/A")

st.divider()

# Sidebar Settings
st.sidebar.image("https://images.pexels.com/lib/api/pexels-white.png", width=100)
st.sidebar.header("⚙️ Pipeline Configuration")
current_day = datetime.datetime.now().weekday()
day_options = {i: DAY_TOPICS[i]['name'] for i in range(7)}
selected_day = st.sidebar.selectbox(
    "Target Topic Day", 
    options=list(day_options.keys()), 
    format_func=lambda x: day_options[x], 
    index=current_day
)

st.sidebar.divider()
st.sidebar.markdown("### 📊 System Health")
st.sidebar.success("Database: Connected")
st.sidebar.success("Pexels API: Active")
st.sidebar.success("Groq API: Ready")

# Initialize session state for post data
if 'post_data' not in st.session_state:
    st.session_state.post_data = None

# Main Tabs
tab1, tab2, tab3 = st.tabs(["⚡ RUN PIPELINE", "🏛️ POST HISTORY", "📝 SYSTEM LOGS"])

with tab1:
    with st.container():
        st.subheader(f"Current Topic: {DAY_TOPICS[selected_day]['name']}")
        st.caption(f"**Strategy:** {DAY_TOPICS[selected_day]['label']}")
        
        col_ctrl, col_prev = st.columns([1, 1.5], gap="large")
        
        with col_ctrl:
            st.markdown("### 🛠️ Controls")
            if st.button("🔍 Generate Professional Post", use_container_width=True, type="secondary"):
                with st.spinner("🧠 AI Researching & Drafting..."):
                    pipeline = AutomationPipeline(dry_run=True)
                    data = pipeline.prepare_post(selected_day)
                    if data:
                        st.session_state.post_data = data
                        st.toast("Post Generated Successfully!")
                    else:
                        st.error("Failed to generate post. Topic might already be posted.")

            if st.session_state.post_data:
                st.info("💡 Review and edit the content on the right before publishing.")
                if st.button("🚀 PUBLISH TO LINKEDIN", type="primary", use_container_width=True):
                    with st.spinner("📤 Transmitting to LinkedIn..."):
                        pipeline = AutomationPipeline()
                        success = pipeline.publish_post(st.session_state.post_data)
                        if success:
                            st.balloons()
                            st.success("🎉 Successfully posted to LinkedIn!")
                            st.session_state.post_data = None
                            st.rerun()
                        else:
                            st.error("❌ Failed to publish. Check system logs.")
            
            st.divider()
            st.markdown("### 🏷️ Target Hashtags")
            tags = DAY_TOPICS[selected_day]['hashtags']
            st.write(" ".join([f"`#{t}`" for t in tags]))

        with col_prev:
            st.markdown("### 📝 Live Preview & Editor")
            if st.session_state.post_data:
                # Content Card
                with st.container(border=True):
                    edited_content = st.text_area(
                        "Post Draft", 
                        value=st.session_state.post_data['final_post'], 
                        height=350,
                        help="You can edit the AI-generated content here before publishing."
                    )
                    st.session_state.post_data['final_post'] = edited_content
                
                # Image Card
                with st.container(border=True):
                    img_path = st.session_state.post_data['image_path']
                    if img_path and os.path.exists(img_path):
                        st.image(str(img_path), caption="Sourced Visual (Pexels)", use_column_width=True)
                    else:
                        st.warning("Visual sourcing pending or failed.")
            else:
                st.info("No active draft. Click 'Generate Professional Post' to begin.")

with tab2:
    st.markdown("### 🏛️ Post Performance Feed")
    if history_data:
        # Sort history: Newest first
        sorted_history = sorted(history_data, key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Display in a grid (3 columns)
        rows = [sorted_history[i:i+3] for i in range(0, len(sorted_history), 3)]
        
        for row in rows:
            cols = st.columns(3)
            for idx, post in enumerate(row):
                with cols[idx]:
                    with st.container(border=True):
                        # 1. Image Thumbnail
                        img_path = post.get('image')
                        if img_path and os.path.exists(img_path):
                            st.image(img_path, use_container_width=True)
                        else:
                            # Placeholder or icon if image missing
                            st.image("https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&h=150", use_container_width=True)
                        
                        # 2. Topic & Meta
                        st.subheader(post.get('topic', 'Untitled Post'))
                        dt = datetime.datetime.fromisoformat(post.get('timestamp', '')) if post.get('timestamp') else None
                        st.caption(f"📅 {dt.strftime('%b %d, %Y | %H:%M') if dt else 'N/A'}")
                        
                        # 3. Content Snippet
                        raw_content = post.get('post', '')
                        snippet = (raw_content[:150] + '...') if len(raw_content) > 150 else raw_content
                        st.write(snippet)
                        
                        # 4. Actions
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if post.get('post_id'):
                                st.link_button("🔗 View Post", f"https://www.linkedin.com/feed/update/{post['post_id']}", use_container_width=True)
                        with col_b:
                            with st.popover("📖 Full Details", use_container_width=True):
                                st.markdown("#### 📝 Post Content")
                                st.markdown(raw_content)
                                if post.get('image_prompt'):
                                    st.divider()
                                    st.markdown("#### 🎨 Image Prompt")
                                    st.caption(post['image_prompt'])
                                
                                st.divider()
                                if st.button("🗑️ Delete from History", key=f"del_{post.get('timestamp')}", type="primary", use_container_width=True):
                                    delete_post(post.get('timestamp'))
                                    st.toast("Post removed from history!")
                                    st.rerun()
    else:
        st.info("No posts recorded yet in the performance feed.")

with tab3:
    st.markdown("### 📝 System Logs")
    l_err, l_succ = st.columns(2)
    
    with l_err:
        st.markdown("#### ❌ Error Log")
        error_log = LOGS_DIR / "error.log"
        if error_log.exists():
            try:
                with open(error_log, 'r') as f:
                    errors = [json.loads(line) for line in f.readlines()]
                st.dataframe(pd.DataFrame(errors[::-1]).head(20), use_container_width=True)
            except:
                st.code(error_log.read_text())
            
            if st.button("Clear Errors"):
                error_log.write_text("")
                st.rerun()
        else:
            st.write("No errors logged.")

    with l_succ:
        st.markdown("#### 💹 Success Log")
        success_log = LOGS_DIR / "success.log"
        if success_log.exists():
            try:
                with open(success_log, 'r') as f:
                    successes = [json.loads(line) for line in f.readlines()]
                st.dataframe(pd.DataFrame(successes[::-1]).head(20), use_container_width=True)
            except:
                st.code(success_log.read_text())
