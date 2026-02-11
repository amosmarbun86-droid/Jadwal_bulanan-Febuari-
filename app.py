import streamlit as st
import pandas as pd
import os
import calendar
from datetime import datetime

# =============================
# KONFIGURASI
# =============================
st.set_page_config(page_title="Jadwal Februari 2026", layout="wide")
st.title("📅 Jadwal Shift - Februari 2026")

# =============================
# LOAD CSV
# =============================
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "jadwal.csv")

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("File jadwal.csv tidak ditemukan.")
    st.stop()

# =============================
# PILIH NAMA
# =============================
nama = st.selectbox("Pilih Karyawan", df["Nama"].unique())
data_karyawan = df[df["Nama"] == nama].iloc[0]

# =============================
# WARNA SHIFT
# =============================
def get_color(value):
    if value == "OFF":
        return "#FF4B4B"
    elif str(value) == "1":
        return "#4CAF50"
    elif str(value) == "2":
        return "#2196F3"
    elif str(value) == "3":
        return "#FF9800"
    else:
        return "#CCCCCC"

# =============================
# BUAT KALENDER
# =============================
year = 2026
month = 2

cal = calendar.monthcalendar(year, month)
days_name = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

# Header Hari
cols = st.columns(7)
for col, day in zip(cols, days_name):
    col.markdown(f"**{day}**")

# Isi Kalender
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            shift_value = data_karyawan[str(day)]
            color = get_color(shift_value)

            cols[i].markdown(
                f"""
                <div style="
                    background-color:{color};
                    padding:15px;
                    border-radius:10px;
                    text-align:center;
                    color:white;
                    font-weight:bold;
                ">
                    {day}<br>
                    {shift_value}
                </div>
                """,
                unsafe_allow_html=True
            )

# =============================
# LEGENDA
# =============================
st.markdown("---")
st.markdown("### Keterangan:")
st.markdown("""
- 🟢 Shift 1  
- 🔵 Shift 2  
- 🟠 Shift 3  
- 🔴 OFF  
""")
