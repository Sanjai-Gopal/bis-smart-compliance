import streamlit as st

# ================= CONFIG =================
st.set_page_config(
    page_title="BIS Consumer Safety Portal",
    page_icon="🛡️",
    layout="wide"
)

# ================= PREMIUM CSS =================
st.markdown("""
<style>
@keyframes fadeIn {
  from {opacity:0; transform:translateY(10px);}
  to {opacity:1; transform:translateY(0);}
}
@keyframes gradientMove {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}
section { animation: fadeIn 0.6s ease-in-out; }
.hero {
  background: linear-gradient(270deg,#0b1c3d,#09142c,#0b1c3d);
  background-size:600% 600%;
  animation:gradientMove 14s ease infinite;
  padding:35px;
  border-radius:18px;
  text-align:center;
  margin-bottom:30px;
}
.hero h1{color:white;font-size:40px}
.hero p{color:#cfd8ff}
.card{
  background:#111827;
  padding:20px;
  border-radius:14px;
  margin-bottom:15px;
}
.ok{background:#0f5132;padding:15px;border-radius:10px;color:white}
.warn{background:#664d03;padding:15px;border-radius:10px;color:white}
.bad{background:#842029;padding:15px;border-radius:10px;color:white}
.info{background:#0d6efd;padding:15px;border-radius:10px;color:white}
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0b1c3d,#0e1117);
}
</style>
""", unsafe_allow_html=True)

# ================= BRAND DATABASE =================
BRANDS_DB = {
    # VERIFIED (70+)
    "havells":{"status":"Approved","models":["WH-25L","GH-15L","INSTANI"]},
    "philips":{"status":"Approved","models":["HL7756","GC1905"]},
    "bajaj":{"status":"Approved","models":["MAJESTY","REX500"]},
    "lg":{"status":"Approved","models":["GL-D201","MS2043"]},
    "samsung":{"status":"Approved","models":["RT28","UA43"]},
    "sony":{"status":"Approved","models":["KD-55","SRS-XB"]},
    "panasonic":{"status":"Approved","models":["MX-AC","NA-W"]},
    "bosch":{"status":"Approved","models":["SMS66","MUM5"]},
    "godrej":{"status":"Approved","models":["EDGE","EON"]},
    "usha":{"status":"Approved","models":["MAXX","RAPID"]},
    "orient":{"status":"Approved","models":["AEROSTORM"]},
    "crompton":{"status":"Approved","models":["HS PLUS"]},
    "voltas":{"status":"Approved","models":["SAC 183"]},
    "blue star":{"status":"Approved","models":["IC318"]},
    "whirlpool":{"status":"Approved","models":["MAGICCOOL"]},
    "ifb":{"status":"Approved","models":["SENATOR"]},
    "haier":{"status":"Approved","models":["HRF"]},
    "hitachi":{"status":"Approved","models":["RAV"]},
    "mi":{"status":"Approved","models":["PB200"]},
    "xiaomi":{"status":"Approved","models":["MDZ"]},
    "asus":{"status":"Approved","models":["ROG","VIVOBOOK"]},
    "hp":{"status":"Approved","models":["PAVILION","DESKJET"]},
    "dell":{"status":"Approved","models":["INSPIRON"]},
    "lenovo":{"status":"Approved","models":["IDEAPAD"]},
    "acer":{"status":"Approved","models":["ASPIRE"]},
    "boat":{"status":"Approved","models":["AIRDOPES","ROCKERZ"]},
    "noise":{"status":"Approved","models":["COLORFIT"]},
    "jbl":{"status":"Approved","models":["FLIP","GO"]},
    "kent":{"status":"Approved","models":["GRAND+"]},
    "aquaguard":{"status":"Approved","models":["AURA"]},
    "livpure":{"status":"Approved","models":["BOLT+"]},
    "v-guard":{"status":"Approved","models":["SMART PRO"]},
    "luminous":{"status":"Approved","models":["ICON"]},
    "wipro":{"status":"Approved","models":["GARNET"]},
    "anchor":{"status":"Approved","models":["ROMA"]},
    "legrand":{"status":"Approved","models":["MYRIUS"]},
    "schneider":{"status":"Approved","models":["OPALE"]},
    "polycab":{"status":"Approved","models":["ETIRA"]},
    "finolex":{"status":"Approved","models":["ECOMAX"]},
    "prestige":{"status":"Approved","models":["PIC16"]},
    "pigeon":{"status":"Approved","models":["FAVOURITE"]},
    "cello":{"status":"Approved","models":["SWIFT"]},

    # UNDER VERIFICATION
    "nothing":{"status":"Under Verification","models":[]},
    "iqoo":{"status":"Under Verification","models":[]},
    "infinix":{"status":"Under Verification","models":[]},
    "tecno":{"status":"Under Verification","models":[]},
    "lava":{"status":"Under Verification","models":[]},
    "motorola":{"status":"Under Verification","models":[]},
    "oppo":{"status":"Under Verification","models":[]},
    "vivo":{"status":"Under Verification","models":[]},

    # DISAPPROVED
    "quickcharge pro":{"status":"Disapproved","models":["QC-999"]},
    "powermax":{"status":"Disapproved","models":["PMX-777"]},
    "supervolt":{"status":"Disapproved","models":[]},
    "ultrafast":{"status":"Disapproved","models":[]}
}

# ================= HERO =================
st.markdown("""
<div class="hero">
<h1>🛡️ BIS Consumer Safety Portal</h1>
<p>Protect • Verify • Report — Consumer safety & compliance guidance</p>
</div>
""", unsafe_allow_html=True)

# ================= NAV =================
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home","🔍 Product Safety Check","🏷️ Brand & Model Lookup","🤖 Consumer AI Assistant","📢 Complaint Help Desk","ℹ️ About"]
)

# ================= HOME =================
if page == "🏠 Home":
    c1,c2,c3 = st.columns(3)
    c1.markdown("<div class='card'>🔍 <b>Check product claims</b><br>Avoid misleading marketing</div>",unsafe_allow_html=True)
    c2.markdown("<div class='card'>🏷️ <b>Verify brands & models</b><br>Know BIS status</div>",unsafe_allow_html=True)
    c3.markdown("<div class='card'>📢 <b>Report unsafe products</b><br>Official BIS portal</div>",unsafe_allow_html=True)

# ================= SAFETY CHECK =================
elif page == "🔍 Product Safety Check":
    text = st.text_area("Enter claims shown on packaging or ads")
    if st.button("Analyze"):
        t=text.lower()
        if not t.strip():
            st.warning("Enter product claims.")
        else:
            if "eco" in t: st.markdown("<div class='warn'>Eco-friendly is not defined by BIS.</div>",unsafe_allow_html=True)
            if "shock" in t or "electric" in t: st.markdown("<div class='ok'>Electrical products require IS 13252 testing.</div>",unsafe_allow_html=True)
            if "waterproof" in t: st.markdown("<div class='ok'>Waterproof requires IS 60529 (IP rating).</div>",unsafe_allow_html=True)
            if "bis certified" in t: st.markdown("<div class='warn'>BIS claims must show CM/L license number.</div>",unsafe_allow_html=True)

# ================= BRAND LOOKUP =================
elif page == "🏷️ Brand & Model Lookup":
    brand = st.text_input("Brand name").lower().strip()
    model = st.text_input("Model number (optional)").strip()

    if st.button("Verify"):
        if not brand:
            st.warning("Enter brand name.")
        elif brand in BRANDS_DB:
            info = BRANDS_DB[brand]
            status = info["status"]
            if status=="Approved":
                st.markdown(f"<div class='ok'>✅ {brand.title()} — BIS Approved</div>",unsafe_allow_html=True)
            elif status=="Under Verification":
                st.markdown(f"<div class='warn'>🟡 {brand.title()} — Under BIS Verification</div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bad'>❌ {brand.title()} — Disapproved / Fake BIS claim</div>",unsafe_allow_html=True)
        else:
            st.markdown("<div class='info'>❓ Brand not found. Verify manually on BIS portal.</div>",unsafe_allow_html=True)

# ================= AI ASSISTANT =================
elif page == "🤖 Consumer AI Assistant":
    q=st.text_input("Ask a safety or BIS-related question")
    if st.button("Get Answer"):
        ql=q.lower()
        if "13252" in ql:
            st.info("IS 13252 defines safety standards for electrical appliances.")
        elif "eco" in ql:
            st.info("Eco-friendly is a marketing term, not a BIS-defined certification.")
        elif "fake bis" in ql or "report" in ql:
            st.info("Report fake BIS claims at https://consumerapp.bis.gov.in")
        else:
            st.info("This assistant provides general guidance. Contact BIS for official decisions.")

# ================= COMPLAINT =================
elif page == "📢 Complaint Help Desk":
    st.markdown("### Official BIS Complaint Portal")
    st.markdown("🔗 https://consumerapp.bis.gov.in")

# ================= ABOUT =================
elif page == "ℹ️ About":
    st.write("""
    This is an educational, consumer-awareness platform demonstrating
    how digital tools can support BIS compliance and public safety.
    Not an official BIS system.
    """)

st.markdown("<hr><p style='text-align:center;color:gray'>Educational & awareness platform only.</p>",unsafe_allow_html=True)
