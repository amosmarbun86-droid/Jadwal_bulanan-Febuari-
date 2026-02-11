import streamlit as st
import pandas as pd
import calendar
import os
from datetime import date
import holidays

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Jadwal Shift",
    layout="wide"
)

# =============================
# CSS (MINIMAL & MOBILE FRIENDLY)
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

.box {
    background:#1F2933;
    border-radius:8px;
    padding:6px 0;
    text-align:center;
    line-height:1.15;
}

.date {
    font-size:12px;
    font-weight:700;
    color:white;
}

.shift {
    font-size:11px;
    font-weight:600;
}

.time {
    font-size:9px;
    color:#D1D5DB;
}

.holiday {
    font-size:9px;
    color:#F87171;
    font-weight:700;
    margin-top:2px;
}
</style>
""", unsafe_allow_html=True)

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
# SESSION STATE BULAN & TAHUN
# =============================
today = date.today()

if "month" not in st.session_state:
    st.session_state.month = today.month
    st.session_state.year = today.year

# =============================
# NAVIGASI BULAN
# =============================
colA, colB, colC = st.columns([1, 3, 1])

with colA:
    if st.button("⏮"):
        if st.session_state.month == 1:
            st.session_state.month = 12
            st.session_state.year -= 1
        else:
            st.session_state.month -= 1

with colC:
    if st.button("⏭"):
        if st.session_state.month == 12:
            st.session_state.month = 1
            st.session_state.year += 1
        else:
            st.session_state.month += 1

bulan = st.session_state.month
tahun = st.session_state.year

st.markdown(
    f"<div class='title'>📅 {calendar.month_name[bulan]} {tahun}</div>",
    unsafe_allow_html=True
)

# =============================
# SHIFT INFO
# =============================
SHIFT_INFO = {
    "1": ("Malam", "22:00–06:00", "#22C55E"),
    "2": ("Pagi", "08:00–17:00", "#3B82F6"),
    "3": ("Sore", "16:00–01:00", "#F59E0B"),
    "OFF": ("OFF", "", "#EF4444")
}

# =============================
# LIBUR NASIONAL
# =============================
ID_HOLIDAYS = holidays.Indonesia()

def cek_libur(tgl: date):
    if tgl in ID_HOLIDAYS:
        return ID_HOLIDAYS[tgl]
    if tgl.weekday() == 6:
        return "Hari Minggu"
    return None

# =============================
# KALENDER
# =============================
cal = calendar.monthcalendar(tahun, bulan)

for week in cal:
    cols = st.columns(7, gap="small")
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            tgl = date(tahun, bulan, day)
            libur = cek_libur(tgl)

            raw = str(row.get(str(day), ""))
            label, jam, color = SHIFT_INFO.get(raw, ("", "", "#6B7280"))

            cols[i].markdown(
                f"""
                <div class="box">
                    <div class="date">{day}</div>
                    <div class="shift" style="color:{color}">{label}</div>
                    <div class="time">{jam}</div>
                    {f"<div class='holiday'>🎌 {libur}</div>" if libur else ""}
                </div>
                """,
                unsafe_allow_html=True
            )
