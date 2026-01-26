import streamlit as st
import re

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="BIS Consumer Safety Portal",
    page_icon="🛡️",
    layout="wide"
)

# ================= PREMIUM CSS =================
st.markdown("""
<style>
@keyframes fade {
  from {opacity:0; transform:translateY(15px);}
  to {opacity:1; transform:translateY(0);}
}
@keyframes glow {
  0%{box-shadow:0 0 5px #1f3cff}
  50%{box-shadow:0 0 18px #1f3cff}
  100%{box-shadow:0 0 5px #1f3cff}
}
body {background-color:#0e1117}
.fade {animation: fade 0.6s ease-in-out}
.hero {
  background: linear-gradient(120deg,#0b1c3d,#0e2a5a);
  padding:40px;
  border-radius:20px;
  color:white;
  margin-bottom:30px;
}
.navcard {
  background:#111827;
  padding:25px;
  border-radius:18px;
  transition:0.3s;
  cursor:pointer;
}
.navcard:hover {
  transform:translateY(-5px);
  animation:glow 2s infinite;
}
.box-ok{background:#0f5132;padding:15px;border-radius:10px;color:white}
.box-warn{background:#664d03;padding:15px;border-radius:10px;color:white}
.box-info{background:#0d6efd;padding:15px;border-radius:10px;color:white}
.box-bad{background:#842029;padding:15px;border-radius:10px;color:white}
</style>
""", unsafe_allow_html=True)

# ================= BRAND DATABASE (SAFE) =================
BRANDS = {
    "havells":"Approved","philips":"Approved","bajaj":"Approved","lg":"Approved",
    "samsung":"Approved","sony":"Approved","panasonic":"Approved","bosch":"Approved",
    "godrej":"Approved","usha":"Approved","orient":"Approved","crompton":"Approved",
    "voltas":"Approved","blue star":"Approved","whirlpool":"Approved","ifb":"Approved",
    "haier":"Approved","hitachi":"Approved","mi":"Approved","xiaomi":"Approved",
    "asus":"Approved","hp":"Approved","dell":"Approved","lenovo":"Approved",
    "acer":"Approved","boat":"Approved","noise":"Approved","jbl":"Approved",
    "kent":"Approved","aquaguard":"Approved","livpure":"Approved","v-guard":"Approved",
    "luminous":"Approved","wipro":"Approved","prestige":"Approved","pigeon":"Approved",
    "cello":"Approved",
    "oppo":"Under Verification","vivo":"Under Verification","iqoo":"Under Verification",
    "nothing":"Under Verification","lava":"Under Verification",
    "quickcharge pro":"Disapproved","powermax":"Disapproved","supervolt":"Disapproved"
}

# ================= SESSION NAV =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= HERO =================
st.markdown("""
<div class="hero fade">
<h1>🛡️ BIS Consumer Safety Portal</h1>
<p>Easy product safety help for everyone — even if English is little</p>
</div>
""", unsafe_allow_html=True)

# ================= NAVIGATION (UNIQUE) =================
c1,c2,c3,c4 = st.columns(4)

if c1.button("🔍 Check Product Safety"):
    st.session_state.page="safety"
if c2.button("🏷️ Check Brand"):
    st.session_state.page="brand"
if c3.button("🤖 Ask Assistant"):
    st.session_state.page="ai"
if c4.button("📢 Complaint Help"):
    st.session_state.page="complaint"

st.markdown("<hr>",unsafe_allow_html=True)

# ================= PRODUCT SAFETY =================
if st.session_state.page=="safety":
    st.markdown("## 🔍 Product Safety Check")
    text = st.text_area("Write what is written on product box (simple English ok)")

    if st.button("Check Safety"):
        t=text.lower()

        if not t.strip():
            st.warning("Please write something about product.")
        else:
            if re.search(r"eco|green|nature",t):
                st.markdown("<div class='box-warn'>Eco-friendly is only a marketing word. BIS does not certify this.</div>",unsafe_allow_html=True)
            if re.search(r"shock|electric|charger|current",t):
                st.markdown("<div class='box-ok'>Electrical items must follow IS 13252 safety rules.</div>",unsafe_allow_html=True)
            if re.search(r"water|rain|ip",t):
                st.markdown("<div class='box-ok'>Waterproof products need IP rating under IS 60529.</div>",unsafe_allow_html=True)
            if re.search(r"bis|certified",t):
                st.markdown("<div class='box-warn'>BIS claims must show license number on product.</div>",unsafe_allow_html=True)

# ================= BRAND CHECK =================
elif st.session_state.page=="brand":
    st.markdown("## 🏷️ Brand Verification")
    brand = st.text_input("Enter brand name (any spelling)")

    if st.button("Verify Brand"):
        if not brand.strip():
            st.warning("Please enter brand name.")
        else:
            key = brand.lower().strip()
            if key in BRANDS:
                status = BRANDS[key]
                if status=="Approved":
                    st.markdown(f"<div class='box-ok'>✅ {brand.title()} is commonly BIS approved.</div>",unsafe_allow_html=True)
                elif status=="Under Verification":
                    st.markdown(f"<div class='box-warn'>🟡 {brand.title()} is under BIS verification.</div>",unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='box-bad'>❌ {brand.title()} has unsafe or fake BIS history.</div>",unsafe_allow_html=True)
            else:
                st.markdown("<div class='box-info'>Brand not in demo list. Check official BIS site to confirm.</div>",unsafe_allow_html=True)

# ================= AI ASSISTANT =================
elif st.session_state.page=="ai":
    st.markdown("## 🤖 Consumer AI Assistant")
    q = st.text_input("Ask in simple English")

    if st.button("Get Help"):
        ql=q.lower()
        if not q.strip():
            st.warning("Ask something.")
        elif "eco" in ql:
            st.info("Eco-friendly is only a marketing word. It is not BIS certified.")
        elif "13252" in ql or "electric" in ql:
            st.info("IS 13252 is safety rule for electrical products.")
        elif "fake" in ql or "cheat" in ql:
            st.info("If you feel cheated, complain on BIS official portal.")
        else:
            st.info("Check product label carefully or verify on BIS website.")

# ================= COMPLAINT =================
elif st.session_state.page=="complaint":
    st.markdown("## 📢 Complaint & Help Desk")
    st.markdown("""
<div class='box-info'>
If product is unsafe or BIS mark is fake, complain here:<br><br>
🔗 <b>https://consumerapp.bis.gov.in</b>
</div>
""",unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<hr>",unsafe_allow_html=True)
st.caption("Educational & awareness platform only. Not an official BIS system.")
