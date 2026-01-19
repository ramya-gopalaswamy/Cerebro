import streamlit as st
import time

# --- SETUP ---
st.set_page_config(page_title="Cerebro: The Interview", page_icon="🧠", layout="wide")

# --- IMAGE PATHS (Local) ---
IMG_JOY = "assets/images/joy.png"
IMG_ANGER = "assets/images/anger.png"
IMG_SADNESS = "assets/images/sadness.png"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    img {
        max-height: 300px;
        object-fit: contain;
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    img:hover {
        transform: scale(1.1);
    }
    .speech-bubble {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        color: #333;
        font-family: sans-serif;
        font-size: 18px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border-left: 10px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ---
if 'step' not in st.session_state:
    st.session_state.step = 1

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.session_state.step == 1:
        st.image(IMG_JOY, width=300)
        st.markdown(f"""
        <div class="speech-bubble" style="border-left-color: #FFD700;">
            <h3>🌟 OH GOOD! YOU'RE HERE!</h3>
            <p>I was getting worried! Okay, we need a new Core Memory. 
            <b>What is the dream job?</b> Tell me, tell me!</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        # Dream Job input with id and label
        st.markdown('<label for="dream-job-input"><b>Enter Dream Job:</b></label>', unsafe_allow_html=True)
        goal = st.text_input("", key="dream-job-input", placeholder="e.g. AI Engineer at Google")
        if st.button("SET GOAL"):
            if goal:
                st.session_state.goal = goal
                st.session_state.step = 2
                st.rerun()
    elif st.session_state.step == 2:
        st.image(IMG_ANGER, width=280)
        st.markdown(f"""
        <div class="speech-bubble" style="border-left-color: #D32F2F;">
            <h3>🔥 '{st.session_state.goal.upper()}'?!</h3>
            <p>Do you have any idea how hard that is? 
            If we're doing this, I'm not accepting failure. 
            <b>Set your pain tolerance levels. NOW.</b></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.slider("Daily Applications (Pain)", 0, 50, 10)
        st.slider("Daily LeetCode (Suffering)", 0, 10, 2)
        if st.button("EXECUTE PLAN"):
            st.balloons()
