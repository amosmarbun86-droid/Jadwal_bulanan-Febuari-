import streamlit as st
import pandas as pd
import os
import calendar

# =============================
# CONFIG PAGE
# =============================
st.set_page_config(page_title="Jadwal Shift Premium", layout="wide")

# =============================
# CUSTOM CSS (MODERN UI)
# =============================
st.markdown("""
<style>
.card {
    background-color: #1E1E2F;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
    text-align: center;
    color: white;
    font-weight: 600;
}
.header-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 25px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.shift-box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

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
# PILIH KARYAWAN
# =============================
nama = st.selectbox("Pilih Karyawan", df["Nama"].unique())
data = df[df["Nama"] == nama].iloc[0]

# =============================
# HEADER INFO CARD
# =============================
st.markdown(f"""
<div class="header-card">
    <h2>{data['Nama']}</h2>
    <p>{data['Jabatan']}</p>
</div>
""", unsafe_allow_html=True)

# =============================
# WARNA SHIFT
# =============================
def get_color(val):
    if val == "OFF":
        return "#E74C3C"
    elif str(val) == "1":
        return "#2ECC71"
    elif str(val) == "2":
        return "#3498DB"
    elif str(val) == "3":
        return "#F39C12"
    return "#7F8C8D"

# =============================
# KALENDER GRID
# =============================
year = 2026
month = 2
cal = calendar.monthcalendar(year, month)

days_name = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

# Header Hari
cols = st.columns(7)
for col, day in zip(cols, days_name):
    col.markdown(f"<div class='card'>{day}</div>", unsafe_allow_html=True)

# Isi Kalender
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            shift_val = data[str(day)]
            color = get_color(shift_val)

            cols[i].markdown(
                f"""
                <div class="shift-box" style="background-color:{color}">
                    <div style="font-size:18px;">{day}</div>
                    <div style="font-size:16px;">{shift_val}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# =============================
# RINGKASAN
# =============================
total_off = sum(1 for d in range(1,29) if data[str(d)] == "OFF")

st.markdown("---")
st.markdown(f"""
<div class="card">
    Total OFF Bulan Ini: {total_off} Hari
</div>
""", unsafe_allow_html=True)

# =============================
# LEGENDA
# =============================
st.markdown("### 🎨 Keterangan Warna")
st.markdown("""
🟢 Shift 1  
🔵 Shift 2  
🟠 Shift 3  
🔴 OFF  
""")
