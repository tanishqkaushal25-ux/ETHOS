import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Entity Timeline Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Main background gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white !important;
    }

    /* Transparent header */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar with frosted glass effect */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
    }

    /* Text styling */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #F8F9FA !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #00B4D8;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0096C7;
        transform: scale(1.05);
    }

    /* Login box */
    .login-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2);
        text-align: center;
        width: 400px;
        margin: auto;
        margin-top: 15vh;
    }

    /* Input fields */
    input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
        border-radius: 8px !important;
    }

    /* Metric cards */
    .metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    color: #000 !important; /* forces black text */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    margin-bottom: 15px;
}

.metric-card h4, 
.metric-card h2 {
    color: #000 !important;
}


    .metric-card h4 {
        font-size: 16px;
        color: #203a43;
    }

    .metric-card h2 {
        font-size: 28px;
        color: rgb(224, 37, 20);
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)


st.title("📊 Entity Timeline Dashboard")
st.write("Interactive dashboard for entity-level timeline analysis.")

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h3 style='text-align:center;'>🔐 Secure Login</h3>", unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    username = st.text_input("👤 Username", key="user")
    password = st.text_input("🔑 Password", type="password", key="pass")

    if st.button("Login"):
        if username == "admin" and password == "password123":
            st.session_state.logged_in = True
            st.success("✅ Login Successful! Loading dashboard...")
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------- LOAD & CLEAN DATA ----------
@st.cache_data
def load_and_clean_data():
    file_path = "../outputs/entity_timeline_sample.csv"
    if not os.path.exists(file_path):
        st.error(f"❌ File not found: {file_path}")
        st.stop()

    df = pd.read_csv(file_path)
    df.columns = [col.strip().lower() for col in df.columns]
    df.replace(["None", "none", "NULL", "null", "NaN", ""], pd.NA, inplace=True)
    df.dropna(how="all", inplace=True)

    if "entity_id" in df.columns:
        df["entity_id"].fillna("Unknown_Entity", inplace=True)
    if "face_id" in df.columns:
        df["face_id"].fillna("Unknown_Face", inplace=True)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    return df

# ---------- LOAD DATA ----------
with st.spinner("🧹 Loading & Cleaning Data..."):
    df = load_and_clean_data()

st.success(f"✅ Data Loaded! Total rows: {len(df):,}")

# ---------- FILTERS ----------
st.sidebar.header("🔍 Filters")

entity_filter = st.sidebar.multiselect(
    "Select Entity ID(s):",
    options=df["entity_id"].unique() if "entity_id" in df.columns else [],
    default=df["entity_id"].unique()[:5] if "entity_id" in df.columns else []
)

face_filter = st.sidebar.multiselect(
    "Select Face ID(s):",
    options=df["face_id"].unique() if "face_id" in df.columns else [],
    default=df["face_id"].unique()[:5] if "face_id" in df.columns else []
)

if "timestamp" in df.columns:
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
else:
    start_date, end_date = None, None

# ---------- APPLY FILTERS ----------
filtered_df = df.copy()
if entity_filter:
    filtered_df = filtered_df[filtered_df["entity_id"].isin(entity_filter)]
if face_filter:
    filtered_df = filtered_df[filtered_df["face_id"].isin(face_filter)]
if start_date and end_date and "timestamp" in df.columns:
    filtered_df = filtered_df[
        (filtered_df["timestamp"].dt.date >= start_date) &
        (filtered_df["timestamp"].dt.date <= end_date)
    ]

# ---------- DATA OVERVIEW ----------
st.subheader("📋 Filtered Dataset Preview")
st.dataframe(filtered_df.head(10))

# ---------- METRICS (White Boxes + Pink Data) ----------
st.subheader("📊 Metrics After Filtering")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Total Unique Entities</h4>
            <h2>{filtered_df["entity_id"].nunique() if "entity_id" in df.columns else 0}</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Total Unique Face IDs</h4>
            <h2>{filtered_df["face_id"].nunique() if "face_id" in df.columns else 0}</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <h4>Earliest Record</h4>
            <h2>{str(filtered_df["timestamp"].min().date()) if "timestamp" in df.columns else "-"}</h2>
        </div>
    """, unsafe_allow_html=True)

# ---------- TIMELINE CHART ----------
st.subheader("📈 Timeline Chart")
if "timestamp" in filtered_df.columns and not filtered_df["timestamp"].isna().all():
    filtered_df["date"] = filtered_df["timestamp"].dt.date
    timeline = filtered_df.groupby("date").size().reset_index(name="events")
    st.line_chart(timeline.set_index("date"))
else:
    st.warning("⚠️ No valid 'timestamp' column for timeline plotting.")

st.write("---")
st.caption("~ Team Metahood")
