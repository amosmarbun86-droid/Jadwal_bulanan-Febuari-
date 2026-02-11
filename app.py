import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
import holidays

st.set_page_config(page_title="Jadwal Shift", layout="wide")

# =====================
# SHIFT CONFIG
# =====================
SHIFT_MAP = {
    "1": {"name": "Malam", "time": "00:00–09:00", "color": "#8B5CF6"},
    "2": {"name": "Pagi", "time": "08:00–17:00", "color": "#22C55E"},
    "3": {"name": "Sore", "time": "16:00–01:00", "color": "#F59E0B"},
    "OFF": {"name": "OFF", "time": "-", "color": "#EF4444"},
}

# =====================
# LOAD CSV
# =====================
df = pd.read_csv("jadwal.csv")

# =====================
# PILIH NAMA
# =====================
nama = st.selectbox("👤 Pilih Nama", df["NAMA"].unique())
row = df[df["NAMA"] == nama].iloc[0]

# =====================
# LIBUR NASIONAL
# =====================
year = datetime.now().year
id_holidays = holidays.Indonesia(years=year)

# =====================
# NOTIF SHIFT BESOK
# =====================
tomorrow = datetime.now() + timedelta(days=1)
tomorrow_day = tomorrow.day

if str(tomorrow_day) in row:
    shift_val = str(row[str(tomorrow_day)])
    shift_info = SHIFT_MAP.get(shift_val, SHIFT_MAP["OFF"])

    st.info(
        f"⏰ Shift Besok ({tomorrow_day}) : "
        f"{shift_info['name']} {shift_info['time']}"
    )

# =====================
# STYLE
# =====================
st.markdown("""
<style>
.card {
    background:#0f172a;
    border-radius:16px;
    padding:14px;
    text-align:center;
    box-shadow:0 4px 14px rgba(0,0,0,.4);
    color:white;
    cursor:pointer;
}
.day {font-size:18px;font-weight:bold;}
.shift {font-size:15px;font-weight:600;margin-top:6px;}
.time {font-size:12px;opacity:.85;}
.holiday {font-size:11px;color:#f87171;}
</style>
""", unsafe_allow_html=True)

# =====================
# MODE 1 TAHUN
# =====================
for month in range(1, 13):

    st.subheader(f"📅 {calendar.month_name[month]} {year}")

    days = calendar.monthrange(year, month)[1]

    cols = st.columns(7)

    for day in range(1, days + 1):

        col = cols[(day - 1) % 7]

        val = str(row.get(str(day), "OFF"))
        shift = SHIFT_MAP.get(val, SHIFT_MAP["OFF"])

        date_obj = datetime(year, month, day)
        holiday_name = id_holidays.get(date_obj)

        with col:

            if st.button(f"{day}", key=f"{month}-{day}"):

                st.popup(
                    f"Detail {day}-{month}-{year}",
                    lambda: st.write(
                        f"""
                        👤 {nama}
                        
                        🕒 {shift['name']}
                        
                        ⏰ {shift['time']}
                        
                        🎉 {holiday_name if holiday_name else 'Bukan hari libur'}
                        """
                    )
                )

            st.markdown(
                f"""
                <div class="card">
                    <div class="day">{day}</div>
                    <div class="shift" style="color:{shift['color']}">
                        {shift['name']}
                    </div>
                    <div class="time">{shift['time']}</div>
                    <div class="holiday">
                        {"🎉 " + holiday_name if holiday_name else ""}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
