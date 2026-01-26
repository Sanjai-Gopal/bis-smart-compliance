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

.nav-btn {
  background:#111827;
  padding:14px 22px;
  border-radius:12px;
  border:1px solid #1f2937;
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

# ================= BRAND DATABASE =================
BRANDS = {
    "havells":"Approved","philips":"Approved","bajaj":"Approved","usha":"Approved","orient":"Approved",
    "crompton":"Approved","godrej":"Approved","lg":"Approved","samsung":"Approved","sony":"Approved",
    "panasonic":"Approved","bosch":"Approved","whirlpool":"Approved","voltas":"Approved",
    "ifb":"Approved","onida":"Approved","haier":"Approved","mi":"Approved","asus":"Approved",
    "hp":"Approved","dell":"Approved","lenovo":"Approved","acer":"Approved","boat":"Approved",
    "wipro":"Approved","v-guard":"Approved","prestige":"Approved","kent":"Approved",
    "quickcharge pro":"Disapproved","powermax":"Disapproved"
}

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= HERO =================
st.markdown("""
<div class="hero fade">
<h1>🛡️ BIS Consumer Safety Portal</h1>
<p>Easy product safety help for everyone — even if English is little</p>
</div>
""", unsafe_allow_html=True)

# ================= NAVIGATION =================
c1,c2,c3,c4,c5 = st.columns(5)
if c1.button("🏠 Home"): st.session_state.page="home"
if c2.button("🔍 Product Safety"): st.session_state.page="safety"
if c3.button("🏷️ Brand Check"): st.session_state.page="brand"
if c4.button("🤖 Ask Assistant"): st.session_state.page="assistant"
if c5.button("📢 Feedback"): st.session_state.page="feedback"

st.divider()

# ================= HOME =================
if st.session_state.page=="home":
    st.markdown('<div class="fade"><h2>👋 Welcome</h2></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section">
    ✔ Check product safety  
    ✔ Detect fake BIS claims  
    ✔ Verify trusted brands  
    ✔ Get help easily  
    </div>
    """, unsafe_allow_html=True)

# ================= PRODUCT SAFETY =================
elif st.session_state.page=="safety":
    st.header("🔍 Product Safety Check")
    text = st.text_area("Write what is written on product box")

    if st.button("Analyze"):
        if not text.strip():
            st.warning("Please write something.")
        else:
            t=text.lower()
            if "eco" in t:
                st.markdown("<div class='box-warn'>Eco-friendly is only a marketing term.</div>",unsafe_allow_html=True)
            if "shock" in t or "electric" in t:
                st.markdown("<div class='box-ok'>Electrical products require IS 13252 testing.</div>",unsafe_allow_html=True)
            if "water" in t:
                st.markdown("<div class='box-ok'>Waterproof claims need IP rating.</div>",unsafe_allow_html=True)

# ================= BRAND CHECK =================
elif st.session_state.page=="brand":
    st.header("🏷️ Brand Verification")
    brand = st.text_input("Enter brand name")

    if st.button("Verify"):
        b=brand.lower().strip()
        if not b:
            st.warning("Enter brand name.")
        elif b in BRANDS:
            status=BRANDS[b]
            if status=="Approved":
                st.markdown(f"<div class='box-ok'>✅ {brand.title()} is commonly BIS approved.</div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='box-bad'>❌ {brand.title()} has safety concerns.</div>",unsafe_allow_html=True)
        else:
            st.markdown("<div class='box-info'>Brand not in demo list. Check official BIS site.</div>",unsafe_allow_html=True)

# ================= AI ASSISTANT =================
elif st.session_state.page=="assistant":
    st.header("🤖 Consumer AI Assistant")
    q=st.text_input("Ask your question")

    if st.button("Get Answer"):
        if "eco" in q.lower():
            st.info("Eco-friendly is not BIS certified.")
        elif "safe" in q.lower():
            st.info("Check BIS mark and trusted brand.")
        else:
            st.info("Please verify on official BIS website.")

# ================= FEEDBACK SYSTEM =================
elif st.session_state.page=="feedback":
    st.header("📢 User Feedback")
    st.markdown("Help us improve this platform.")

    rating = st.select_slider(
        "Rate your experience",
        options=["⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"]
    )

    comment = st.text_area("Your feedback (optional)")

    if st.button("Submit Feedback"):
        st.success("Thank you! Your feedback is recorded 🙏")

# ================= FOOTER =================
st.divider()
st.caption("Educational & awareness platform only. Not an official BIS system.")
