import streamlit as st
import pandas as pd
import os
import calendar
from datetime import date

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="Jadwal Shift", layout="wide")

# =============================
# TRY LOAD HOLIDAY LIB
# =============================
try:
    import holidays
    ID_HOLIDAY = holidays.Indonesia()
except:
    ID_HOLIDAY = None

# =============================
# CSS MINIMAL
# =============================
st.markdown("""
<style>
body { background:#0E1117; }
.title { text-align:center; font-size:16px; font-weight:600; }
.sub { text-align:center; font-size:12px; color:#9CA3AF; margin-bottom:6px; }
.box {
    background:#1F2933;
    border-radius:6px;
    padding:5px 0;
    text-align:center;
    line-height:1.15;
}
.date { font-size:11px; font-weight:700; }
.shift { font-size:10px; font-weight:600; }
.time { font-size:9px; color:#9CA3AF; }
.holiday { font-size:9px; color:#F87171; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# =============================
# LOAD DATA
# =============================
BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "jadwal.csv"))

nama = st.selectbox("Nama", df["Nama"].unique())
row = df[df["Nama"] == nama].iloc[0]
st.markdown(f"<div class='sub'>{row['Jabatan']}</div>", unsafe_allow_html=True)

# =============================
# PILIH BULAN & TAHUN
# =============================
bulan_nama = list(calendar.month_name)[1:]
bulan_map = {name: i+1 for i, name in enumerate(bulan_nama)}

col1, col2 = st.columns(2)
with col1:
    bulan_pilih = st.selectbox("Bulan", bulan_nama, index=date.today().month - 1)
with col2:
    tahun_pilih = st.selectbox("Tahun", list(range(2024, 2031)), index=2)

bulan = bulan_map[bulan_pilih]

st.markdown(
    f"<div class='title'>📅 {bulan_pilih} {tahun_pilih}</div>",
    unsafe_allow_html=True
)

# =============================
# SHIFT INFO
# =============================
SHIFT_INFO = {
    "1": ("Malam", "00:00–09:00", "#22C55E"),
    "2": ("Pagi",  "08:00–17:00", "#3B82F6"),
    "3": ("Sore",  "16:00–01:00", "#F59E0B"),
    "OFF": ("OFF", "", "#EF4444")
}

# =============================
# CEK LIBUR
# =============================
def get_holiday(d):
    if ID_HOLIDAY and d in ID_HOLIDAY:
        return ID_HOLIDAY[d]
    if d.weekday() == 6:
        return "Hari Minggu"
    return None

# =============================
# KALENDER
# =============================
cal = calendar.monthcalendar(tahun_pilih, bulan)

for week in cal:
    cols = st.columns(7, gap="small")
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            d = date(tahun_pilih, bulan, day)
            holiday = get_holiday(d)

            raw = str(row.get(str(day), ""))
            label, jam, color = SHIFT_INFO.get(raw, ("", "", "#6B7280"))

            cols[i].markdown(
                f"""
                <div class="box">
                    <div class="date">{day}</div>
                    <div class="shift" style="color:{color}">{label}</div>
                    <div class="time">{jam}</div>
                    {"<div class='holiday'>🎌 "+holiday+"</div>" if holiday else ""}
                </div>
                """,
                unsafe_allow_html=True
            )
