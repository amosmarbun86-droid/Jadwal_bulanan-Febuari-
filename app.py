import streamlit as st
import pandas as pd
import calendar
from io import BytesIO

st.set_page_config(page_title="Jadwal Februari 2026", layout="centered")

st.title("📅 JADWAL KERJA")
st.subheader("FEBRUARI 2026")

# ==========================
# DATA SESUAI GAMBAR
# ==========================

karyawan = [
    ("Jhody ansyah Setiawan", "SHIFT LEAD"),
    ("Deni Simanjuntak", "SHIFT LEAD"),
    ("Sucris Juliyisno Panjaitan", "TEAM LEAD"),
    ("Marlin Simboling", "TEAM LEAD"),
    ("Wilfan Ependi Sibuea", "TEAM LEAD"),
    ("Judika Hutagaol", "ADMIN / TRACER"),
    ("Monang Josua Silaban", "SOC PIC"),
    ("Alex Sanro Manalu", "DED OPERATOR"),
    ("AMOS", "DED OPERATOR"),
    ("EGI SIMANUNGKALIT", "DED OPERATOR"),
    ("ROBERT NAINGGOLAN", "DED OPERATOR"),
    ("SHALMAN TEGAR HUTASOIT", "DED OPERATOR"),
    ("FREDRIK HUTAJULU", "DED OPERATOR"),
    ("JONNI PARDOMUAN SITUMEANG", "DED OPERATOR"),
    ("Lindon Rajagukguk", "DED OPERATOR"),
    ("PEBY AGUSTINUS TARIGAN", "DED OPERATOR"),
    ("YOSUA KEVIN RAJAGUKGUK", "DED OPERATOR"),
    ("TONGAM JANUARI PARLINDUNGAN SIANIPAR", "SOC PIC"),
]

bulan = 2
tahun = 2026
jumlah_hari = calendar.monthrange(tahun, bulan)[1]

# ==========================
# POLA SHIFT SESUAI GAMBAR
# ==========================

pola = [
    "OFF", "3", "3", "3",
    "OFF", "2", "2", "2",
    "OFF", "1", "1", "1"
]

data = []

for idx, (nama, title) in enumerate(karyawan):
    row = {
        "NO": idx + 1,
        "NAMA": nama,
        "TITLE": title
    }

    for i in range(jumlah_hari):
        shift = pola[(i + idx) % len(pola)]
        row[str(i+1)] = shift

    data.append(row)

df = pd.DataFrame(data)

# ==========================
# REKAP
# ==========================

df["Shift 1"] = df.apply(lambda x: list(x).count("1"), axis=1)
df["Shift 2"] = df.apply(lambda x: list(x).count("2"), axis=1)
df["Shift 3"] = df.apply(lambda x: list(x).count("3"), axis=1)
df["OFF"] = df.apply(lambda x: list(x).count("OFF"), axis=1)

# ==========================
# WARNA SHIFT
# ==========================

def warna_shift(val):
    if val == "OFF":
        return "background-color: red; color: white"
    elif val == "1":
        return "background-color: #90EE90"
    elif val == "2":
        return "background-color: #FFFF99"
    elif val == "3":
        return "background-color: #ADD8E6"
    return ""

styled_df = df.style.applymap(warna_shift)

# ==========================
# TAMPILAN MOBILE
# ==========================

tab1, tab2 = st.tabs(["📋 Jadwal", "📊 Rekap"])

with tab1:
    st.dataframe(styled_df, use_container_width=True, height=500)

with tab2:
    st.dataframe(
        df[["NAMA", "Shift 1", "Shift 2", "Shift 3", "OFF"]],
        use_container_width=True
    )

# ==========================
# DOWNLOAD EXCEL
# ==========================

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

excel_data = to_excel(df)

st.download_button(
    "📥 Download Excel",
    data=excel_data,
    file_name="Jadwal_Februari_2026.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)
