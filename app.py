import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Event Discovery Platform | Powered by Avi Win", layout="wide", page_icon="💃")

# Navigation using session state
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

def set_page(name):
    st.session_state.page = name

# Premium Slate & Sky Blue Aesthetic (Reverted)
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Headers */
    h1 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    
    h2, h3 {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling - Back to Dark but with optimized label contrast */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Optimized Sidebar Labels */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] div, [data-testid="stSidebar"] p {
        color: #e2e8f0 !important; /* Lighter color for better readability */
        font-weight: 500 !important;
    }
    
    /* Input field text inside sidebar */
    [data-testid="stSidebar"] .stTextInput input, [data-testid="stSidebar"] .stMultiSelect {
        color: #ffffff !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #38bdf8;
        color: #ffffff !important; /* Force white text */
        border-radius: 8px;
        border: none;
        font-weight: 700;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        background-color: #0ea5e9;
        color: #ffffff !important;
    }

    /* Metrics and Cards */
    .stMetric label, .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important; /* Force white text for metrics */
    }
    .stMetric {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .next-event-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        border: 1px solid #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# Helper: Infer date from weekday
def infer_actual_date(weekday_str):
    if not weekday_str or not isinstance(weekday_str, str): return None
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        if len(weekday_str) > 5 and any(char.isdigit() for char in weekday_str):
            return weekday_str
        target_day = -1
        for i, d in enumerate(days):
            if d.lower() in weekday_str.lower():
                target_day = i
                break
        if target_day == -1: return None
        today = datetime.now()
        today_idx = today.weekday()
        days_ahead = target_day - today_idx
        if days_ahead < 0: days_ahead += 7
        return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    except:
        return None

# Function to load data
@st.cache_data
def load_data():
    # Try multiple possible paths for the database
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend', 'pipeline', 'dance_events.db'),
        os.path.join('backend', 'pipeline', 'dance_events.db'),
        'backend/pipeline/dance_events.db',
        'dance_events.db'
    ]
    
    db_path = None
    for p in possible_paths:
        if os.path.exists(p):
            db_path = p
            break
    
    # Last resort: Search for it
    if not db_path:
        for root, dirs, files in os.walk('.'):
            if 'dance_events.db' in files:
                db_path = os.path.join(root, 'dance_events.db')
                break
            
    if not db_path:
        return pd.DataFrame()
    
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT name, date, start_time, city, venue, organizer, website, source FROM events", conn)
        conn.close()
        
        # Enrich data with inferred dates
        df['calculated_date'] = df['date'].apply(infer_actual_date)
        return df
    except Exception as e:
        st.error(f"Error reading database at {db_path}: {e}")
        return pd.DataFrame()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown(f"<h2 style='color:#8b0000; text-align:center;'>AVI WIN</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

if st.sidebar.button("📊 Events Dashboard", use_container_width=True):
    set_page('Dashboard')
if st.sidebar.button("ℹ️ About the Solution", use_container_width=True):
    set_page('About')

st.sidebar.markdown("---")

# Main Content Logic
if st.session_state.page == 'Dashboard':
    st.title("Event discovery platform, powered by Avi Win")
    
    df = load_data()
    
    if df.empty:
        st.warning("No database found. Please run the scraper pipeline first.")
    else:
        # Filters in Sidebar (only for Dashboard)
        st.sidebar.header("🔍 Search & Filters")
        selected_source = st.sidebar.multiselect("Data Source", options=df['source'].unique(), default=df['source'].unique())
        selected_city = st.sidebar.multiselect("City", options=df['city'].unique(), default=df['city'].unique())
        search_term = st.sidebar.text_input("Search event name...", "")

        filtered_df = df[
            (df['source'].isin(selected_source)) & 
            (df['city'].isin(selected_city)) &
            (df['name'].str.contains(search_term, case=False, na=False))
        ]

        # Highlight: Next Event
        st.subheader("🔥 Spotlight: Next Dance Opportunity")
        next_event = df[df['calculated_date'].notna()].sort_values('calculated_date').iloc[0] if not df.empty else None
        if next_event is not None:
            st.markdown(f"""
            <div class="next-event-card">
                <h2 style="color:#d4af37 !important; border:none; padding:0;">{next_event['name']}</h2>
                <p style="font-size:1.1em;">📅 <b>Date:</b> {next_event['date']} ({next_event['calculated_date']}) | 🕒 <b>Time:</b> {next_event['start_time'] or 'N/A'}</p>
                <p style="font-size:1.1em;">📍 <b>City:</b> {next_event['city']} | 🏛️ <b>Venue:</b> {next_event['venue']}</p>
                <p style="margin-top:15px;"><a href="{next_event['website']}" target="_blank" style="background:#d4af37; color:#1a1a1a; padding:10px 20px; border-radius:5px; text-decoration:none; font-weight:bold;">GET TICKETS / INFO</a></p>
            </div>
            """, unsafe_allow_html=True)

        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Live Events", len(df))
        m2.metric("Filtered View", len(filtered_df))
        m3.metric("Partners", len(df['source'].unique()))

        # Map
        st.subheader("🗺️ Global Reach")
        city_coords = {
            'London': [51.5074, -0.1278], 'Paris': [48.8566, 2.3522],
            'Barcelona': [41.3851, 2.1734], 'Buenos Aires': [-34.6037, -58.3816],
            'Perpignan': [42.6887, 2.8948], 'Lomma': [55.6726, 13.0706],
            'Moszna': [50.4419, 17.7661], 'Alexandroupoli': [40.8476, 25.8739]
        }
        map_data = filtered_df['city'].apply(lambda x: city_coords.get(x, None)).dropna().tolist()
        if map_data:
            st.map(pd.DataFrame(map_data, columns=['lat', 'lon']), zoom=1)

        # Table
        st.subheader("📅 Curated Listings")
        st.dataframe(
            filtered_df[['name', 'date', 'calculated_date', 'start_time', 'city', 'venue', 'website', 'source']],
            use_container_width=True,
            column_config={
                "website": st.column_config.LinkColumn("Info"),
                "calculated_date": st.column_config.DateColumn("Date")
            }
        )

elif st.session_state.page == 'About':
    st.title("Engineering the Solution")
    
    st.markdown("""
    ### Technical Architecture
    The **Avi Win Event Discovery Platform** is an end-to-end data pipeline designed for high-fidelity event aggregation.
    
    #### 1. Distributed Ingestion
    We utilize a specialized Python scraping fleet:
    - **Playwright Engine**: Mimics human interaction to navigate Single Page Applications (SPAs) like *TangoCat*. It handles JS rendering and dynamic popups.
    - **BeautifulSoup Engine**: Optimized for high-speed parsing of hierarchical HTML structures found in legacy sites like *Milongas-In*.
    
    #### 2. Normalization & Enrichment
    Raw data is converted into a unified format:
    - **Date Inference**: A custom algorithm calculates actual calendar dates from relative names (e.g., "Next Thursday").
    - **Schema Mapping**: Diverse field names are standardized into a global schema.
    
    #### 3. Integrity & Storage
    - **Deduplication Engine**: Uses SHA-256 hashing to ensure no redundant listings enter the database.
    - **SQLite Persistence**: High-performance local storage for reliable data access.
    
    #### 4. Delivery
    - **Streamlit Frontend**: A reactive interface providing real-time filtering and geographic visualization.
    """)
    
    if st.button("⬅️ Back to Dashboard"):
        set_page('Dashboard')

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-style: italic;'>Designed for the heart of the Tango community • Powered by Avi Win</div>", unsafe_allow_html=True)
