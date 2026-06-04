import os
import requests
import streamlit as st
from textSummarizer.pipeline.prediction import PredictionPipeline

backend_url = os.getenv("BACKEND_URL", "").strip()
use_backend = bool(backend_url)

st.set_page_config(
    page_title="Smart Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f1f3c 100%);
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 58, 95, 0.9) 100%);
        border-right: 2px solid rgba(34, 211, 238, 0.3);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding: 2rem 1.5rem;
    }
    
    .stSidebar [data-testid="stHeading"] {
        color: #f1f5f9;
        font-weight: 700;
    }
    
    .main-header {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .main-header img {
        width: 60px;
        height: 60px;
    }
    
    .title-section {
        margin-bottom: 3rem;
    }
    
    .title-section h1 {
        color: #f1f5f9;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .title-section p {
        color: #94a3b8;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .instruction-text {
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(249, 115, 22, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(74, 222, 128, 0.1) 100%);
        border: 2px solid #4ade80;
        border-radius: 0.75rem;
        padding: 1.5rem;
        color: #86efac;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    
    .content-section {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.3) 0%, rgba(15, 23, 42, 0.5) 100%);
        border: 1px solid rgba(34, 211, 238, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .content-header {
        color: #f1f5f9;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .content-header::before {
        content: "●";
        color: #22d3ee;
        font-size: 1.5rem;
    }
    
    .comparison-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 768px) {
        .comparison-container {
            grid-template-columns: 1fr;
        }
    }
    
    .text-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 0.75rem;
        padding: 1.5rem;
        color: #cbd5e1;
        line-height: 1.7;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .text-box::-webkit-scrollbar {
        width: 6px;
    }
    
    .text-box::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.3);
        border-radius: 3px;
    }
    
    .text-box::-webkit-scrollbar-thumb {
        background: rgba(34, 211, 238, 0.4);
        border-radius: 3px;
    }
    
    .text-box::-webkit-scrollbar-thumb:hover {
        background: rgba(34, 211, 238, 0.6);
    }
    
    .stats-row {
        background: rgba(30, 58, 95, 0.4);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-top: 1.5rem;
        color: #94a3b8;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #22d3ee;
    }
    
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(34, 211, 238, 0.3) !important;
        color: #e2e8f0 !important;
        border-radius: 0.5rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #64748b !important;
    }
    
    .stRadio {
        color: #e2e8f0;
    }
    
    .stRadio > label {
        color: #cbd5e1 !important;
    }
    
    .stRadio [role="radio"] {
        accent-color: #22d3ee;
    }
    
    .stFileUploader {
        color: #cbd5e1;
    }
    
    .stExpander {
        background: rgba(30, 58, 95, 0.3);
        border: 1px solid rgba(34, 211, 238, 0.2);
        border-radius: 0.5rem;
    }
    
    .stExpander > summary {
        color: #e2e8f0;
        font-weight: 600;
    }
    
    .stExpander > summary:hover {
        color: #22d3ee;
    }
    
    .stInfo, .stSuccess, .stWarning, .stError {
        background: rgba(30, 58, 95, 0.4) !important;
        border: 1px solid rgba(34, 211, 238, 0.2) !important;
        color: #cbd5e1 !important;
        border-radius: 0.5rem !important;
    }
    
    hr {
        border-color: rgba(34, 211, 238, 0.2);
        margin: 2rem 0;
    }
    
    .metric {
        background: rgba(30, 58, 95, 0.3);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    [data-testid="metric-container"] {
        background: rgba(30, 58, 95, 0.3);
        border: 1px solid rgba(34, 211, 238, 0.15);
        border-radius: 0.5rem;
        padding: 1rem !important;
    }
    
    [data-testid="metric-container"] > div:first-child {
        color: #94a3b8;
        font-size: 0.875rem;
    }
    
    [data-testid="metric-container"] > div:last-child {
        color: #22d3ee;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_predictor():
    if use_backend:
        return None
    return PredictionPipeline()

predictor = load_predictor()

if "text_input" not in st.session_state:
    st.session_state.text_input = ""

sample_text = (
    "The midnight fog turned Cairo into a ghost town, but inside Tarek's cab, the air was warm with shared dreams. "
    "His young passenger, Youssef, talked passionately about the software company he had just launched that very evening. "
    "When they reached the destination, Youssef stepped out, completely unaware that his priceless laptop had slipped onto the seat. "
    "Tarek didn't hesitate; he spun the car around, raced up four flights of stairs, and handed the machine back to the terrified life. "
    "Youssef wept with relief, promising the honest driver a job for life when his empire finally took over the world."
)

# Main Header
st.markdown(
    """
    <div class="title-section">
        <h1>📝 Smart Text Summarizer</h1>
        <p>Convert long text, meeting notes, or conversations into concise, readable summaries.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="instruction-text">Use the sidebar to paste your text or upload a text file. Then click <strong>Summarize</strong> to generate a clean summary instantly.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 📥 Input")
    st.markdown("---")
    
    input_mode = st.radio("Choose input type", ["Paste text", "Upload text file"], index=0)
    
    if input_mode == "Upload text file":
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file is not None:
            st.session_state.text_input = uploaded_file.read().decode("utf-8", errors="ignore")
    else:
        st.session_state.text_input = st.text_area(
            "Enter text to summarize",
            value=st.session_state.text_input,
            height=280,
            placeholder="Paste your conversation or document here...",
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Use sample text", use_container_width=True):
            st.session_state.text_input = sample_text
            st.rerun()
    
    with col2:
        summarize_request = st.button("Summarize", use_container_width=True)

text_input = st.session_state.text_input

if summarize_request:
    if not text_input or text_input.strip() == "":
        st.warning("Please enter some text or upload a file before summarizing.")
    else:
        with st.spinner("Generating your summary..."):
            try:
                summary = predictor.predict(text_input)
                words = len(text_input.split())
                summary_words = len(summary.split())
                compression_ratio = round((1 - summary_words / words) * 100, 1) if words > 0 else 0
                
                st.markdown(
                    '<div class="success-box">✓ Summary generated successfully!</div>',
                    unsafe_allow_html=True,
                )
                
                st.markdown(
                    """
                    <div class="comparison-container">
                        <div class="content-section">
                            <div class="content-header">Original Text</div>
                            <div class="text-box">""" + text_input.replace("\"", "&quot;") + """</div>
                        </div>
                        <div class="content-section">
                            <div class="content-header">Summary</div>
                            <div class="text-box">""" + summary.replace("\"", "&quot;") + """</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                st.markdown(
                    f"""
                    <div class="stats-row">
                        <div class="stat-item">
                            <div class="stat-label">Original Words</div>
                            <div class="stat-value">{words}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Summary Words</div>
                            <div class="stat-value">{summary_words}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">Compression Ratio</div>
                            <div class="stat-value">{compression_ratio}%</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as error:
                st.error(f"Failed to summarize text: {error}")
else:
    st.markdown(
        """
        <div class="content-section">
            <p style="color: #cbd5e1; margin: 0;">
                Paste text or upload a file, then click <strong>Summarize</strong> to see the result.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

with st.expander("ℹ️ Why this summarizer?", expanded=False):
    st.write(
        "This frontend uses the same trained summarization pipeline as your FastAPI backend. "
        "It loads the model once and keeps the interface clean and responsive for quick text summarization."
    )

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Input type", input_mode)
with col2:
    st.metric("Model", "Backend" if use_backend else "Local")
with col3:
    st.metric("Status", "Active")
