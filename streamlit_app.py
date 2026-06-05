import streamlit as st
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from google import genai
import datetime as dt

# ========== API SETUP ==========
API_KEY = "AQ.Ab8RN6LXgM2CW0uj28o5ZBZnts3NNQStWra6tgXcyrkgcFWB1w"
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# Nakshatras
nakshatras = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

st.set_page_config(page_title="True Kundali Decoder", layout="wide")

# Title
st.markdown("""
<div style='text-align: center; background: linear-gradient(135deg, #FFD700, #FF9933); padding: 20px; border-radius: 15px'>
    <h1 style='color: #0F0F1A'>🔱 TRUE KUNDALI DECODER (AI-POWERED) 🔱</h1>
    <p style='color: #1A1A2E'>🌍 हिंदू · इस्लामिक · रोमन · माया — चारों सभ्यताओं के ज्योतिष का अद्वितीय संगम 🌎</p>
    <p>Developed by <strong>B A KHAN</strong> (+91-9935310660)</p>
</div>
""", unsafe_allow_html=True)

# Mode selection
mode = st.radio("📌 Mode:", ["Single (Only Me)", "Match (Two Persons)"], horizontal=True)

# Person 1
with st.expander("👤 PERSON 1 DETAILS", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name1 = st.text_input("Full Name", "User 1")
        date1 = st.text_input("Date (DD/MM/YYYY)", "04/07/1996")
        time1 = st.text_input("Time (HH:MM)", "09:10")
    with col2:
        lat1 = st.number_input("Latitude", value=19.0760, format="%.4f")
        lon1 = st.number_input("Longitude", value=72.8777, format="%.4f")
        tz1 = st.text_input("Timezone (±HH:MM)", "+05:30")

# Person 2 (if match mode)
if mode == "Match (Two Persons)":
    with st.expander("👤 PERSON 2 DETAILS", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name2 = st.text_input("Full Name (Person 2)", "User 2")
            date2 = st.text_input("Date (DD/MM/YYYY) - Person 2", "15/08/1998")
            time2 = st.text_input("Time (HH:MM) - Person 2", "14:30")
        with col2:
            lat2 = st.number_input("Latitude (Person 2)", value=19.0760, format="%.4f")
            lon2 = st.number_input("Longitude (Person 2)", value=72.8777, format="%.4f")
            tz2 = st.text_input("Timezone (±HH:MM) - Person 2", "+05:30")
else:
    name2 = None

# Function to get chart
def get_chart(date_str, time_str, lat, lon, tz):
    parts = date_str.split('/')
    formatted = f"{parts[2]}/{parts[1]}/{parts[0]}"
    dt_obj = Datetime(formatted, time_str, tz)
    pos = GeoPos(float(lat), float(lon))
    return Chart(dt_obj, pos)

# Function to call AI
def call_ai(prompt):
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI सेवा व्यस्त है: {str(e)[:100]}"

# Generate button
if st.button("🔮 GENERATE ALL REPORTS", use_container_width=True):
    with st.spinner("⏳ Generating reports (15-20 seconds)..."):
        try:
            chart1 = get_chart(date1, time1, lat1, lon1, tz1)
            planets1 = {p: chart1.get(getattr(const, p.upper())).lon for p in ['sun','moon','mars','mercury','jupiter','venus','saturn']}
            lagna1 = chart1.get(const.ASC).lon
            age1 = dt.datetime.now().year - int(date1.split('/')[2])
            
            if mode == "Match (Two Persons)":
                chart2 = get_chart(date2, time2, lat2, lon2, tz2)
                planets2 = {p: chart2.get(getattr(const, p.upper())).lon for p in ['sun','moon','mars','mercury','jupiter','venus','saturn']}
                lagna2 = chart2.get(const.ASC).lon
            
            base_style = """तुम एक सार्वभौमिक ज्योतिषी हो। हिंदू, इस्लामिक, रोमन और माया सभ्यताओं के ज्योतिष का मिश्रण हो। भाषा हिंदी होगी।"""
            
            # Generate all prompts and results
            tabs = st.tabs(["📋 KUNDALI", "💑 MATCHING", "🕌 MUHURTHA", "🪐 TRANSIT", "🔢 NUMEROLOGY", "💼 CAREER", "❤️ HEALTH"])
            
            # Kundali
            with tabs[0]:
                prompt = f"{base_style}\n{name1} के लिए विश्लेषण: ग्रह {planets1}, लग्न {lagna1:.1f}°, आयु {age1}. सरल हिंदी में बताओ: पिछला जन्म, वर्तमान, भविष्य"
                result = call_ai(prompt)
                st.markdown(result)
            
            # Matching (if match mode)
            with tabs[1]:
                if mode == "Match (Two Persons)":
                    prompt = f"{base_style}\n{name1} और {name2} का मिलान: {name1}: ग्रह {planets1}, {name2}: ग्रह {planets2}. गुना स्कोर, अनुकूलता, उपाय बताओ"
                    result = call_ai(prompt)
                else:
                    result = "Single mode selected. Switch to Match mode for compatibility report."
                st.markdown(result)
            
            # Muhurtha
            with tabs[2]:
                prompt = f"{base_style}\n{name1} के लिए शुभ मुहूर्त बताओ"
                st.markdown(call_ai(prompt))
            
            # Transit
            with tabs[3]:
                prompt = f"{base_style}\n{name1} के लिए गोचर विश्लेषण बताओ"
                st.markdown(call_ai(prompt))
            
            # Numerology
            with tabs[4]:
                total = sum(int(d) for d in date1 if d.isdigit())
                lucky = total % 9 or 9
                prompt = f"{base_style}\n{name1}, जन्म {date1}, भाग्यांक {lucky} के अनुसार विश्लेषण"
                st.markdown(call_ai(prompt))
            
            # Career
            with tabs[5]:
                prompt = f"{base_style}\nग्रह {planets1}, लग्न {lagna1:.1f}° के अनुसार करियर"
                st.markdown(call_ai(prompt))
            
            # Health
            with tabs[6]:
                prompt = f"{base_style}\nग्रह {planets1}, लग्न {lagna1:.1f}° के अनुसार स्वास्थ्य"
                st.markdown(call_ai(prompt))
            
            st.success(f"✅ {name1} के लिए सभी रिपोर्ट तैयार!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}\n\nकृपया सही जानकारी दर्ज करें")