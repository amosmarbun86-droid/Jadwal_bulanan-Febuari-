import streamlit as st
import pandas as pd
import os

# =============================
# KONFIGURASI HALAMAN
# =============================
st.set_page_config(
    page_title="Jadwal Shift Februari 2026",
    layout="wide"
)

st.title("📅 Jadwal Shift Februari 2026")

# =============================
# LOAD FILE CSV (AMAN UNTUK CLOUD)
# =============================
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "jadwal.csv")

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("❌ File jadwal.csv tidak ditemukan. Pastikan file ada di folder yang sama dengan app.py")
    st.stop()

# =============================
# TAMPILKAN DATA
# =============================
st.success("✅ Data berhasil dimuat")

st.dataframe(df, use_container_width=True)

# =============================
# FILTER BERDASARKAN NAMA
# =============================
st.subheader("🔍 Filter Jadwal Karyawan")

nama_list = df["Nama"].unique()
selected_nama = st.selectbox("Pilih Nama:", nama_list)

filtered_df = df[df["Nama"] == selected_nama]

st.dataframe(filtered_df, use_container_width=True)
