import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jadwal Bulanan", page_icon="📅", layout="wide")

st.title("📅 Jadwal Bulanan Februari 2026")

# Load data
df = pd.read_csv("jadwal.csv")

# Pilih nama untuk melihat jadwal
nama_list = df["Nama"].tolist()
selected_name = st.selectbox("Pilih Nama", nama_list)

st.subheader(f"Jadwal {selected_name}")

# Ambil data orang yang dipilih
row = df[df["Nama"] == selected_name]
# Drop kolom Nama & Jabatan untuk menampilkan shift
shift_data = row.drop(columns=["Nama", "Jabatan"]).T
shift_data.columns = ["Shift"]
st.table(shift_data)
