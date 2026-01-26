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
@keyframes fadeIn {
  from {opacity:0; transform:translateY(15px);}
  to {opacity:1; transform:translateY(0);}
}
@keyframes gradientMove {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}
.fade { animation: fadeIn 0.6s ease-in-out; }

.hero {
  background: linear-gradient(270deg,#0b1c3d,#0e2a5a,#0b1c3d);
  background-size:600% 600%;
  animation:gradientMove 14s ease infinite;
  padding:45px;
  border-radius:20px;
  text-align:center;
  color:white;
  margin-bottom:35px;
}

.navcard {
  background:#111827;
  padding:25px;
  border-radius:18px;
  transition:0.3s;
  cursor:pointer;
}
.navcard:hover {
  transform:translateY(-6px);
  box-shadow:0 12px 30px rgba(0,0,0,0.4);
}

.box-ok{background:#0f5132;padding:16px;border-radius:12px;color:white}
.box-warn{background:#664d03;padding:16px;border-radius:12px;color:white}
.box-bad{background:#842029;padding:16px;border-radius:12px;color:white}
.box-info{background:#0d6efd;padding:16px;border-radius:12px;color:white}

.section {
  background:#0f172a;
  padding:25px;
  border-radius:18px;
  margin-bottom:25px;
}
</style>
""", unsafe_allow_html=True)

# ================= BRAND DATABASE (SAFE DEMO) =================
BRANDS = {
    # APPROVED (50+ famous brands)
    "havells":"Approved","philips":"Approved","bajaj":"Approved","usha":"Approved","orient":"Approved",
    "crompton":"Approved","godrej":"Approved","lg":"Approved","samsung":"Approved","sony":"Approved",
    "panasonic":"Approved","bosch":"Approved","siemens":"Approved","whirlpool":"Approved",
    "voltas":"Approved","blue star":"Approved","ifb":"Approved","onida":"Approved","haier":"Approved",
    "hitachi":"Approved","mi":"Approved","xiaomi":"Approved","redmi":"Approved","asus":"Approved",
    "hp":"Approved","dell":"Approved","lenovo":"Approved","acer":"Approved","realme":"Approved",
    "boat":"Approved","noise":"Approved","jbl":"Approved","tata power":"Approved","luminous":"Approved",
    "microtek":"Approved","v-guard":"Approved","syska":"Approved","wipro":"Approved","anchor":"Approved",
    "legrand":"Approved","schneider":"Approved","polycab":"Approved","finolex":"Approved",
    "prestige":"Approved","pigeon":"Approved","cello":"Approved","kent":"Approved","aquaguard":"Approved",
    "livpure":"Approved",

    # UNDER VERIFICATION
    "nothing":"Under Verification","iqoo":"Under Verification","infinix":"Under Verification",
    "tecno":"Under Verification","lava":"Under Verification","motorola":"Under Verification",
    "oppo":"Under Verification","vivo":"Under Verification",

    # DISAPPROVED / FAKE
    "quickcharge pro":"Disapproved","powermax":"Disapproved","supervolt":"Disapproved",
    "ultrafast":"Disapproved","megapower":"Disapproved"
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

# ================= UNIQUE NAVIGATION =================
c1,c2,c3,c4,c5 = st.columns(5)

if c1.button("🏠 Home"):
    st.session_state.page="home"
if c2.button("🔍 Product Safety"):
    st.session_state.page="safety"
if c3.button("🏷️ Brand Check"):
    st.session_state.page="brand"
if c4.button("🤖 Ask Assistant"):
    st.session_state.page="assistant"
if c5.button("📢 Help / Complaint"):
    st.session_state.page="complaint"

st.markdown("<hr>", unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page=="home":
    st.markdown("## 👋 Welcome", class_="fade")
    st.markdown("""
    <div class="section">
    This website helps **normal consumers** understand:
    <br>✔ Product safety  
    <br>✔ Fake BIS claims  
    <br>✔ Trusted brands  
    <br>✔ Where to complain officially  
    </div>
    """, unsafe_allow_html=True)

    a,b,c = st.columns(3)
    a.markdown("<div class='navcard'>🔍 <b>Check safety</b><br>Type what is written on product box</div>",unsafe_allow_html=True)
    b.markdown("<div class='navcard'>🏷️ <b>Check brand</b><br>Know if brand is trusted</div>",unsafe_allow_html=True)
    c.markdown("<div class='navcard'>📢 <b>Report problem</b><br>Go to official BIS portal</div>",unsafe_allow_html=True)

# ================= PRODUCT SAFETY =================
elif st.session_state.page=="safety":
    st.markdown("## 🔍 Product Safety Check")
    st.markdown("Write anything shown on product box (simple English ok).")

    text = st.text_area("Example: fast charger, shock proof, eco friendly")

    if st.button("Check Safety"):
        if not text.strip():
            st.warning("Please write something about product.")
        else:
            t=text.lower()
            found=False

            if re.search(r"eco|green|nature",t):
                st.markdown("<div class='box-warn'>Eco-friendly is only a marketing word. BIS does not certify this.</div>",unsafe_allow_html=True)
                found=True
            if re.search(r"shock|electric|charger|current|power",t):
                st.markdown("<div class='box-ok'>Electrical products must follow IS 13252 safety rules.</div>",unsafe_allow_html=True)
                found=True
            if re.search(r"water|rain|ip|splash",t):
                st.markdown("<div class='box-ok'>Waterproof claims need IP rating under IS 60529.</div>",unsafe_allow_html=True)
                found=True
            if re.search(r"child|baby|kids",t):
                st.markdown("<div class='box-ok'>Child safety products must meet IS 9873.</div>",unsafe_allow_html=True)
                found=True
            if re.search(r"bis|certified|approved",t):
                st.markdown("<div class='box-warn'>BIS claim must show CM/L license number.</div>",unsafe_allow_html=True)
                found=True

            if not found:
                st.markdown("<div class='box-info'>No major safety claims found. Check BIS mark on product.</div>",unsafe_allow_html=True)

# ================= BRAND CHECK =================
elif st.session_state.page=="brand":
    st.markdown("## 🏷️ Brand Verification")
    brand = st.text_input("Enter brand name (any spelling)")

    if st.button("Verify Brand"):
        if not brand.strip():
            st.warning("Please enter brand name.")
        else:
            key=brand.lower().strip()
            if key in BRANDS:
                status=BRANDS[key]
                if status=="Approved":
                    st.markdown(f"<div class='box-ok'>✅ {brand.title()} is a commonly BIS-approved brand.</div>",unsafe_allow_html=True)
                elif status=="Under Verification":
                    st.markdown(f"<div class='box-warn'>🟡 {brand.title()} is under BIS verification.</div>",unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='box-bad'>❌ {brand.title()} has fake / unsafe BIS history.</div>",unsafe_allow_html=True)
            else:
                st.markdown("<div class='box-info'>Brand not in demo list. Please check official BIS website.</div>",unsafe_allow_html=True)

# ================= AI ASSISTANT =================
elif st.session_state.page=="assistant":
    st.markdown("## 🤖 Consumer AI Assistant")
    st.markdown("Ask in simple English. Example: *is eco friendly safe?*")

    q=st.text_input("Your question")

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please ask something.")
        else:
            ql=q.lower()
            if "eco" in ql:
                st.info("Eco-friendly is a marketing word. BIS does not certify it.")
            elif "shock" in ql or "electric" in ql:
                st.info("Electrical items must be BIS tested for safety.")
            elif "fake" in ql or "cheat" in ql:
                st.info("If you feel cheated, complain on BIS official portal.")
            elif "safe" in ql:
                st.info("Check BIS mark and brand before buying.")
            else:
                st.info("Check product label carefully or verify on BIS website.")

# ================= COMPLAINT =================
elif st.session_state.page=="complaint":
    st.markdown("## 📢 Complaint & Help Desk")
    st.markdown("""
    <div class="section">
    If product is unsafe or BIS mark is fake, complain here:
    <br><br>
    🔗 <b>https://consumerapp.bis.gov.in</b>
    <br><br>
    This will open the official Government of India BIS complaint portal.
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Educational & awareness platform only. Not an official BIS system.")
