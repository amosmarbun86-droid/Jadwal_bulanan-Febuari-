import streamlit as st
import pandas as pd
import os
import calendar
from datetime import date, timedelta

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="Jadwal Shift", layout="wide")

# =============================
# CSS SUPER COMPACT
# =============================
st.markdown("""
<style>
body { background:#0E1117; }
.title {
    text-align:center;
    font-size:16px;
    font-weight:600;
    margin-bottom:4px;
}
.sub {
    text-align:center;
    font-size:12px;
    color:#9CA3AF;
    margin-bottom:8px;
}
.alert {
    background:#111827;
    border-left:4px solid #22C55E;
    padding:8px 12px;
    border-radius:8px;
    margin-bottom:10px;
    font-size:12px;
}
.day-btn button {
    width:100%;
    padding:4px 0;
    border-radius:6px;
    font-size:10px;
    font-weight:600;
    color:white;
    border:none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📅 Februari 2026</div>", unsafe_allow_html=True)

# =============================
# LOAD DATA
# =============================
BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "jadwal.csv"))

# =============================
# PILIH KARYAWAN
# =============================
nama = st.selectbox("Nama", df["Nama"].unique())
row = df[df["Nama"] == nama].iloc[0]

st.markdown(f"<div class='sub'>{row['Jabatan']}</div>", unsafe_allow_html=True)

# =============================
# SHIFT INFO
# =============================
SHIFT_INFO = {
    "1": ("Malam", "00:00–06:00", "#16A34A"),
    "2": ("Pagi",  "08:00–16:00", "#2563EB"),
    "3": ("Sore",  "16:00–01:00", "#F59E0B"),
    "OFF": ("OFF", "-", "#DC2626")
}

# =============================
# 🔔 NOTIFIKASI SHIFT BESOK
# =============================
today = date.today()
tomorrow = today + timedelta(days=1)

if tomorrow.month == 2 and tomorrow.day <= 28:
    raw = str(row[str(tomorrow.day)])
    label, jam, _ = SHIFT_INFO.get(raw)

    st.markdown(f"""
    <div class="alert">
        🔔 <b>Shift Besok</b> ({tomorrow.strftime('%d %B %Y')})<br>
        <b>{label}</b> &nbsp; {jam}
    </div>
    """, unsafe_allow_html=True)

# =============================
# SESSION STATE (POPUP)
# =============================
if "selected_day" not in st.session_state:
    st.session_state.selected_day = None

# =============================
# KALENDER TAPABLE
# =============================
cal = calendar.monthcalendar(2026, 2)

for week in cal:
    cols = st.columns(7, gap="small")
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            raw = str(row[str(day)])
            label, jam, color = SHIFT_INFO.get(raw)

            with cols[i]:
                if st.button(f"{day}\n{label}", key=f"d{day}"):
                    st.session_state.selected_day = day

                st.markdown(
                    f"""
                    <style>
                    div[data-testid="stButton"][id="d{day}"] button {{
                        background:{color};
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

# =============================
# POPUP DETAIL
# =============================
if st.session_state.selected_day:
    d = st.session_state.selected_day
    raw = str(row[str(d)])
    label, jam, _ = SHIFT_INFO.get(raw)

    with st.expander(f"📌 Detail {d} Februari 2026", expanded=True):
        st.markdown(f"""
        **Nama:** {row['Nama']}  
        **Jabatan:** {row['Jabatan']}  
        **Shift:** {label}  
        **Jam Kerja:** {jam}
        """)
        if st.button("Tutup"):
            st.session_state.selected_day = None
            st.experimental_rerun()
