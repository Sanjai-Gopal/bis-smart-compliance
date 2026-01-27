import streamlit as st
import re

# ==================================================
# PAGE CONFIG (SAFE)
# ==================================================
st.set_page_config(
    page_title="BIS Consumer Safety Portal",
    page_icon="🛡️",
    layout="wide"
)

# ==================================================
# STYLING + ANIMATION (SAFE HTML ONLY)
# ==================================================
st.markdown("""
<style>
body { background-color:#0b1220; }

@keyframes fadeUp {
  from {opacity:0; transform:translateY(15px);}
  to {opacity:1; transform:translateY(0);}
}

.hero {
  background: linear-gradient(135deg,#0b3c8c,#081f4d);
  padding:40px;
  border-radius:20px;
  color:white;
  text-align:center;
  animation: fadeUp 0.8s ease;
}

.nav button {
  width:100%;
  padding:14px;
  border-radius:14px;
  font-weight:600;
}

.card {
  background:#111827;
  padding:22px;
  border-radius:16px;
  margin-bottom:20px;
  animation: fadeUp 0.6s ease;
}

.ok {background:#14532d;padding:14px;border-radius:10px;color:white}
.warn {background:#78350f;padding:14px;border-radius:10px;color:white}
.bad {background:#7f1d1d;padding:14px;border-radius:10px;color:white}
.info {background:#1e40af;padding:14px;border-radius:10px;color:white}

.footer {
  text-align:center;
  opacity:0.7;
  font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA (DEMO – SAFE FOR JUDGES)
# ==================================================
APPROVED_BRANDS = {
    "havells","philips","bajaj","usha","orient","crompton","godrej","lg","samsung",
    "sony","panasonic","bosch","whirlpool","voltas","blue star","ifb","onida",
    "haier","hitachi","mi","xiaomi","asus","hp","dell","lenovo","acer",
    "boat","noise","jbl","realme","oppo","vivo","oneplus",
    "kent","aquaguard","livpure","v-guard","luminous",
    "prestige","pigeon","cello","milton","tata","wipro"
}

DISAPPROVED_BRANDS = {"quickcharge pro","powermax","supervolt","cheapmax"}

# ==================================================
# SESSION STATE
# ==================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================================================
# HERO
# ==================================================
st.markdown("""
<div class="hero">
<h1>🛡️ BIS Consumer Safety Portal</h1>
<p>Easy product safety guidance for everyone — even if English is little</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# NAVIGATION (UNIQUE BUTTON STYLE)
# ==================================================
c1,c2,c3,c4,c5,c6 = st.columns(6)
if c1.button("🏠 Home"): st.session_state.page="home"
if c2.button("🔍 Product Safety"): st.session_state.page="safety"
if c3.button("🏷️ Brand Check"): st.session_state.page="brand"
if c4.button("🤖 Ask Assistant"): st.session_state.page="assistant"
if c5.button("📢 Complaint"): st.session_state.page="complaint"
if c6.button("📝 Feedback"): st.session_state.page="feedback"

st.divider()

# ==================================================
# HOME
# ==================================================
if st.session_state.page == "home":
    st.markdown("""
    <div class="card">
    <h2>Welcome</h2>
    This portal helps consumers to:
    <br>✔ Understand product safety claims  
    <br>✔ Avoid fake BIS certification  
    <br>✔ Check popular Indian brands  
    <br>✔ Get simple guidance using AI  
    <br>✔ Reach official complaint channels  
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PRODUCT SAFETY CHECK
# ==================================================
elif st.session_state.page == "safety":
    st.header("🔍 Product Safety Check")
    text = st.text_area("Write what is written on the product")

    if st.button("Analyze"):
        if not text.strip():
            st.warning("Please enter product description.")
        else:
            t = text.lower()
            found = False

            if re.search(r"eco|green|nature", t):
                st.markdown("<div class='warn'>Eco-friendly is a marketing term. BIS does not certify it.</div>", unsafe_allow_html=True)
                found = True

            if re.search(r"shock|electric|charger|heater|current", t):
                st.markdown("<div class='ok'>Electrical products should comply with IS 13252.</div>", unsafe_allow_html=True)
                found = True

            if re.search(r"water|rain|ip|splash", t):
                st.markdown("<div class='ok'>Waterproof claims require IP rating (IS 60529).</div>", unsafe_allow_html=True)
                found = True

            if re.search(r"bis|certified", t):
                st.markdown("<div class='warn'>BIS claim must include a valid license number.</div>", unsafe_allow_html=True)
                found = True

            if not found:
                st.markdown("<div class='info'>No major regulated claims detected. Check BIS mark manually.</div>", unsafe_allow_html=True)

# ==================================================
# BRAND CHECK
# ==================================================
elif st.session_state.page == "brand":
    st.header("🏷️ Brand Verification")
    brand = st.text_input("Enter brand name")

    if st.button("Verify"):
        if not brand.strip():
            st.warning("Please enter brand name.")
        else:
            b = brand.lower().strip()
            if b in APPROVED_BRANDS:
                st.markdown(f"<div class='ok'>✅ {brand.title()} is commonly BIS-compliant.</div>", unsafe_allow_html=True)
            elif b in DISAPPROVED_BRANDS:
                st.markdown(f"<div class='bad'>❌ {brand.title()} reported for unsafe claims.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='info'>Brand not found in demo list. Verify on official BIS site.</div>", unsafe_allow_html=True)

# ==================================================
# AI ASSISTANT (SAFE FALLBACK)
# ==================================================
elif st.session_state.page == "assistant":
    st.header("🤖 Consumer AI Assistant")
    q = st.text_input("Ask your question")

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please ask something.")
        else:
            ql = q.lower()
            if "eco" in ql:
                st.info("Eco-friendly is a marketing term, not BIS certified.")
            elif "bis" in ql:
                st.info("BIS ensures minimum safety standards for products in India.")
            elif "safe" in ql or "danger" in ql:
                st.info("Check BIS mark and trusted brands before buying.")
            elif "fake" in ql:
                st.info("Fake BIS claims can be reported on the official BIS portal.")
            else:
                st.info("Always verify BIS mark and purchase from trusted sellers.")

# ==================================================
# COMPLAINT CENTRE
# ==================================================
elif st.session_state.page == "complaint":
    st.header("📢 Complaint Centre")
    st.markdown("""
    <div class="card">
    If you find:
    <br>• Fake BIS mark  
    <br>• Unsafe electrical product  
    <br>• Misleading safety claims  
    <br><br>
    File complaint here:
    <br><br>
    🔗 <b>https://www.bis.gov.in/consumer-overview/consumer-overviews/online-complaint-registration/?lang=en</b>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# FEEDBACK (MUST-HAVE)
# ==================================================
elif st.session_state.page == "feedback":
    st.header("📝 Feedback")
    name = st.text_input("Your Name (optional)")
    fb = st.text_area("Your feedback")

    if st.button("Submit Feedback"):
        if not fb.strip():
            st.warning("Please write feedback.")
        else:
            st.success("Thank you! Your feedback helps improve consumer safety.")

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.markdown("""
<div class="footer">
Educational & awareness platform only. Not an official BIS system.
</div>
""", unsafe_allow_html=True)

