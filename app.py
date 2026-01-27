import streamlit as st
import re

# ================= BASIC CONFIG =================
st.set_page_config(
    page_title="BIS Consumer Safety Portal",
    page_icon="🛡️",
    layout="wide"
)

# ================= STYLING =================
st.markdown("""
<style>
@keyframes fadeUp {
  from {opacity:0; transform:translateY(12px);}
  to {opacity:1; transform:translateY(0);}
}
@keyframes bgMove {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}
.fade {animation: fadeUp 0.6s ease-in-out}

.hero {
  background: linear-gradient(270deg,#0b1c3d,#0e2a5a,#0b1c3d);
  background-size:600% 600%;
  animation:bgMove 15s ease infinite;
  padding:40px;
  border-radius:18px;
  color:white;
  text-align:center;
  margin-bottom:30px;
}

.nav-btn button {
  width:100%;
  padding:14px;
  border-radius:12px;
}

.card {
  background:#0f172a;
  padding:22px;
  border-radius:16px;
  margin-bottom:20px;
}

.ok{background:#0f5132;padding:14px;border-radius:10px;color:white}
.warn{background:#664d03;padding:14px;border-radius:10px;color:white}
.bad{background:#842029;padding:14px;border-radius:10px;color:white}
.info{background:#0d6efd;padding:14px;border-radius:10px;color:white}
</style>
""", unsafe_allow_html=True)

# ================= BRAND DATA (SAFE DEMO) =================
APPROVED_BRANDS = {
    "havells","philips","bajaj","usha","orient","crompton","godrej","lg","samsung",
    "sony","panasonic","bosch","whirlpool","voltas","blue star","ifb","onida",
    "haier","hitachi","mi","xiaomi","asus","hp","dell","lenovo","acer","boat",
    "noise","jbl","kent","aquaguard","livpure","v-guard","luminous","wipro",
    "prestige","pigeon","cello"
}

DISAPPROVED_BRANDS = {"quickcharge pro","powermax","supervolt"}

# ================= SESSION NAV =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= HERO =================
st.markdown("""
<div class="hero fade">
<h1>🛡️ BIS Consumer Safety Portal</h1>
<p>Simple product safety guidance for everyone</p>
</div>
""", unsafe_allow_html=True)

# ================= NAVIGATION =================
c1,c2,c3,c4,c5 = st.columns(5)
if c1.button("🏠 Home"): st.session_state.page="home"
if c2.button("🔍 Product Safety"): st.session_state.page="safety"
if c3.button("🏷️ Brand Check"): st.session_state.page="brand"
if c4.button("🤖 Ask Assistant"): st.session_state.page="assistant"
if c5.button("📢 Complaint Centre"): st.session_state.page="complaint"

st.divider()

# ================= HOME =================
if st.session_state.page=="home":
    st.markdown("## Welcome", class_="fade")
    st.markdown("""
    <div class="card">
    This platform helps consumers:
    <br>✔ Understand product safety claims  
    <br>✔ Avoid fake BIS markings  
    <br>✔ Check commonly trusted brands  
    <br>✔ Reach official complaint channels easily  
    </div>
    """, unsafe_allow_html=True)

# ================= PRODUCT SAFETY =================
elif st.session_state.page=="safety":
    st.header("🔍 Product Safety Check")
    text = st.text_area("Write what is written on the product (simple English is OK)")

    if st.button("Check Safety"):
        if not text.strip():
            st.warning("Please enter product information.")
        else:
            t = text.lower()
            shown = False

            if re.search(r"eco|green|nature", t):
                st.markdown("<div class='warn'>“Eco-friendly” is a marketing term. BIS does not certify it.</div>", unsafe_allow_html=True)
                shown = True

            if re.search(r"shock|electric|charger|current|power", t):
                st.markdown("<div class='ok'>Electrical products should comply with IS 13252 safety standard.</div>", unsafe_allow_html=True)
                shown = True

            if re.search(r"water|rain|ip|splash", t):
                st.markdown("<div class='ok'>Waterproof claims require IP rating as per IS 60529.</div>", unsafe_allow_html=True)
                shown = True

            if re.search(r"bis|certified|approved", t):
                st.markdown("<div class='warn'>BIS claim must include a valid CM/L license number.</div>", unsafe_allow_html=True)
                shown = True

            if not shown:
                st.markdown("<div class='info'>No major regulated safety claims detected. Please check BIS mark manually.</div>", unsafe_allow_html=True)

# ================= BRAND CHECK =================
elif st.session_state.page=="brand":
    st.header("🏷️ Brand Verification")
    brand = st.text_input("Enter brand name")

    if st.button("Verify Brand"):
        if not brand.strip():
            st.warning("Please enter a brand name.")
        else:
            b = brand.lower().strip()
            if b in APPROVED_BRANDS:
                st.markdown(f"<div class='ok'>✅ {brand.title()} is commonly associated with BIS-compliant products.</div>", unsafe_allow_html=True)
            elif b in DISAPPROVED_BRANDS:
                st.markdown(f"<div class='bad'>❌ {brand.title()} has reported fake or unsafe claims.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='info'>Brand not found in demo registry. Please verify on official BIS website.</div>", unsafe_allow_html=True)

# ================= AI ASSISTANT =================
elif st.session_state.page=="assistant":
    st.header("🤖 Consumer Assistant")
    q = st.text_input("Ask your question (simple English is fine)")

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please ask a question.")
        else:
            ql = q.lower()

            if "eco" in ql:
                st.info("Eco-friendly is a marketing term and not a BIS certification.")
            elif "safe" in ql or "danger" in ql:
                st.info("Check for BIS mark and trusted brand before buying.")
            elif "bis" in ql:
                st.info("BIS ensures minimum safety standards for certain products in India.")
            elif "fake" in ql or "complain" in ql:
                st.info("You can report fake BIS claims through the official BIS complaint portal.")
            else:
                st.info("For safety, always check BIS mark and verify through official sources.")

# ================= COMPLAINT CENTRE =================
elif st.session_state.page=="complaint":
    st.header("📢 Complaint Centre")
    st.markdown("""
    <div class="card">
    If you suspect:
    <br>• Fake BIS certification  
    <br>• Unsafe electrical product  
    <br>• Misleading safety claims  
    <br><br>
    Please submit a complaint through the official BIS consumer portal.
    <br><br>
    🔗 <b>https://consumerapp.bis.gov.in</b>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.divider()
st.caption("Educational & awareness platform only. Not an official BIS system.")
