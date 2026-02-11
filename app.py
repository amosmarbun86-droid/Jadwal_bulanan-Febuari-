import streamlit as st
import pandas as pd
import os
import calendar

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="Jadwal Shift", layout="wide")

# =============================
# CSS SUPER COMPACT (HP)
# =============================
st.markdown("""
<style>
body {
    background-color:#0E1117;
}
.title {
    text-align:center;
    font-size:16px;
    font-weight:600;
    margin-bottom:6px;
}
.sub {
    text-align:center;
    font-size:12px;
    color:#9CA3AF;
    margin-bottom:10px;
}
.box {
    padding:4px 0;
    border-radius:6px;
    text-align:center;
    font-size:11px;
    font-weight:600;
    color:white;
}
select {
    font-size:13px !important;
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

st.markdown(
    f"<div class='sub'>{row['Jabatan']}</div>",
    unsafe_allow_html=True
)

# =============================
# WARNA SHIFT (MINIMAL)
# =============================
def color(v):
    return {
        "OFF": "#DC2626",
        "1": "#16A34A",
        "2": "#2563EB",
        "3": "#F59E0B"
    }.get(str(v), "#374151")

# =============================
# KALENDER SUPER PADAT
# =============================
cal = calendar.monthcalendar(2026, 2)

for week in cal:
    cols = st.columns(7, gap="small")
    for i, day in enumerate(week):
        if day == 0:
            cols[i].write("")
        else:
            val = row[str(day)]
            cols[i].markdown(
                f"""
                <div class="box" style="background:{color(val)}">
                    {day}<br>{val}
                </div>
                """,
                unsafe_allow_html=True
            )

# =============================
# RINGKASAN MINI
# =============================
off_count = sum(row[str(d)] == "OFF" for d in range(1, 29))
st.markdown(
    f"<div class='sub'>OFF: {off_count} hari</div>",
    unsafe_allow_html=True
)
