import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Jadwal Februari 2026", layout="centered")

st.title("📅 JADWAL KERJA")
st.subheader("FEBRUARI 2026")

# ==========================
# LOAD FILE CSV
# ==========================

df = pd.read_csv("Jadwal.csv")

# Tambahkan kolom NO
df.insert(0, "NO", range(1, len(df) + 1))

# ==========================
# WARNA SHIFT
# ==========================

def warna_shift(val):
    if str(val) == "OFF":
        return "background-color: red; color: white"
    elif str(val) == "1":
        return "background-color: #90EE90"
    elif str(val) == "2":
        return "background-color: #FFFF99"
    elif str(val) == "3":
        return "background-color: #ADD8E6"
    return ""

styled_df = df.style.applymap(warna_shift)

st.dataframe(styled_df, use_container_width=True, height=500)

# ==========================
# DOWNLOAD CSV
# ==========================

csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv_buffer.getvalue(),
    file_name="Jadwal_Februari_2026.csv",
    mime="text/csv",
    use_container_width=True
)
