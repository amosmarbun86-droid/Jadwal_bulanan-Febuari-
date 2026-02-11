import streamlit as st
import pandas as pd
import calendar
from datetime import date, timedelta

st.set_page_config(page_title="Jadwal Shift", layout="wide")

# =====================
# LOAD USERS
# =====================
users = pd.read_csv("users.csv")

# =====================
# LOGIN
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login Jadwal Shift")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users[(users.username == u) & (users.password == p)]
        if not user.empty:
            st.session_state.login = True
            st.session_state.role = user.iloc[0].role
            st.session_state.nama = user.iloc[0].nama
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username / Password salah")

    st.stop()

# =====================
# AUTO TAHUN & CSV
# =====================
tahun = date.today().year
df = pd.read_csv(f"jadwal_{tahun}.csv")

SHIFT_INFO = {
    "1": ("🌙 Malam", "22:00–06:00", "#6366F1"),
    "2": ("🌅 Pagi", "08:00–16:00", "#22C55E"),
    "3": ("🌇 Sore", "16:00–01:00", "#F97316"),
    "OFF": ("❌ OFF", "", "#EF4444")
}

LIBUR_NASIONAL = {
    "01-01": "🎉 Tahun Baru",
    "02-10": "🎉 Imlek",
    "03-29": "🎉 Nyepi",
    "04-18": "🎉 Wafat Isa Almasih",
    "05-01": "🎉 Hari Buruh",
    "08-17": "🎉 HUT RI 🇮🇩",
    "12-25": "🎉 Natal"
}

# =====================
# HEADER
# =====================
st.sidebar.success(f"👤 {st.session_state.nama}")
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.title(f"📅 Jadwal Shift {tahun}")

# =====================
# FILTER USER
# =====================
if st.session_state.role == "user":
    df = df[df["NAMA"] == st.session_state.nama]

# =====================
# NOTIFIKASI BESOK
# =====================
besok = date.today() + timedelta(days=1)
tgl_besok = str(besok.day)

st.info(f"🔔 Shift BESOK ({besok.strftime('%d %B %Y')})")
for _, r in df.iterrows():
    kode = str(r[tgl_besok])
    nama, jam, _ = SHIFT_INFO.get(kode, ("", "", ""))
    st.write(f"• {r['NAMA']} → {nama} {jam}")

# =====================
# KALENDER 1 TAHUN
# =====================
for bulan in range(1, 13):
    st.markdown("---")
    st.subheader(f"📆 {calendar.month_name[bulan]}")

    hari_bulan = calendar.monthrange(tahun, bulan)[1]
    cols = st.columns(7)
    hari = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

    for i, h in enumerate(hari):
        cols[i].markdown(f"**{h}**")

    start = date(tahun, bulan, 1).weekday()
    row = cols

    for i in range(start):
        row[i].markdown(" ")

    for tgl in range(1, hari_bulan + 1):
        col = (start + tgl - 1) % 7
        label = str(tgl)

        key_libur = f"{bulan:02d}-{tgl:02d}"
        if key_libur in LIBUR_NASIONAL:
            label += f"\n{LIBUR_NASIONAL[key_libur]}"

        if row[col].button(label, key=f"{bulan}-{tgl}"):
            st.session_state.popup = (bulan, tgl)

        if col == 6:
            row = st.columns(7)

# =====================
# POPUP DETAIL
# =====================
if "popup" in st.session_state:
    bulan, tgl = st.session_state.popup
    st.markdown("---")
    st.subheader(f"📌 Detail Shift {tgl} {calendar.month_name[bulan]}")

    for _, r in df.iterrows():
        kode = str(r[str(tgl)])
        nama, jam, warna = SHIFT_INFO.get(kode, ("", "", "#999"))

        st.markdown(
            f"""
            <div style="padding:10px;
                        border-left:5px solid {warna};
                        background:#0f172a;
                        margin-bottom:6px;
                        border-radius:8px;
                        color:white;">
                <b>{r['NAMA']}</b><br>
                <span style="color:{warna}">{nama}</span><br>
                <small>{jam}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("❌ Tutup"):
        del st.session_state.popup

# =====================
# ADMIN PANEL
# =====================
if st.session_state.role == "admin":
    st.sidebar.markdown("## 🛠️ Admin Panel")

    upload = st.sidebar.file_uploader("Upload CSV Baru", type="csv")
    if upload:
        with open(f"jadwal_{tahun}.csv", "wb") as f:
            f.write(upload.getbuffer())
        st.sidebar.success("CSV berhasil diupdate")

    st.sidebar.download_button(
        "⬇️ Download CSV",
        data=df.to_csv(index=False),
        file_name=f"jadwal_{tahun}.csv"
    )
