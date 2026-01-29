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
  from {opacity:0; transform:translateY(18px);}
  to {opacity:1; transform:translateY(0);}
}
@keyframes glow {
  0% { box-shadow: 0 0 0px rgba(59,130,246,0.2); }
  50% { box-shadow: 0 0 18px rgba(59,130,246,0.35); }
  100% { box-shadow: 0 0 0px rgba(59,130,246,0.2); }
}
.hero {
  background: linear-gradient(135deg,#0b3c8c,#081f4d);
  padding:40px;
  border-radius:22px;
  color:white;
  text-align:center;
  animation: fadeUp 0.9s ease;
}
.card {
  background:#111827;
  padding:24px;
  border-radius:18px;
  margin-bottom:22px;
  animation: fadeUp 0.6s ease;
}
.ok {background:#14532d;padding:16px;border-radius:12px;color:white}
.warn {background:#78350f;padding:16px;border-radius:12px;color:white}
.bad {background:#7f1d1d;padding:16px;border-radius:12px;color:white}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA
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
# NAVIGATION
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
    ✔ Understand product safety claims<br>
    ✔ Avoid fake BIS certification<br>
    ✔ Check popular Indian brands<br>
    ✔ Get AI guidance<br>
    ✔ Reach official complaint channels
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# PRODUCT SAFETY CHECK (FIXED)
# ==================================================
elif st.session_state.page == "safety":
    st.header("🔍 Product Safety Check")
    text = st.text_area("Describe the product")

    if st.button("Analyze Safety"):
        if not text.strip():
            st.warning("Please enter product info")
            st.stop()

        t = text.lower()
        category = "General Consumer Product"
        safety_status = "🟢 Generally Safe"
        confidence = "High"
        recommendation = "Safe after verification"
        style = "ok"

        reasons = []
        bis_references = []

        if any(k in t for k in ["charger","adapter","electric"]):
            category = "Electrical Product"
            safety_status = "🟡 Needs Verification"
            confidence = "Medium"
            recommendation = "Use with caution"
            style = "warn"
            reasons.append("Electrical products may cause shock or fire.")
            bis_references.append("IS 13252")

        if any(k in t for k in ["toy","child","baby"]):
            category = "Child Product"
            safety_status = "🟡 Needs Verification"
            confidence = "Medium"
            recommendation = "Verify before use"
            style = "warn"
            reasons.append("Child products require strict BIS compliance.")
            bis_references.append("IS 9873")

        if "100% safe" in t:
            safety_status = "🔴 High Risk"
            confidence = "Low"
            recommendation = "Not recommended"
            style = "bad"
            reasons.append("Unrealistic claims detected.")

        if "bis" not in t:
            reasons.append("No BIS reference mentioned.")

        st.markdown(
            f"""
            <div class="{style}">
            <b>Category:</b> {category}<br>
            <b>Status:</b> {safety_status}<br>
            <b>Confidence:</b> {confidence}<br><br>
            <b>Recommendation:</b> {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("🔎 How this was decided"):
            for r in reasons:
                st.write("•", r)

        st.markdown("### 📜 BIS References")
        for ref in set(bis_references):
            st.write("•", ref)

# ==================================================
# BRAND CHECK
# ==================================================
elif st.session_state.page == "brand":
    st.header("🏷️ Brand Check")
    brand = st.text_input("Brand name")

    if st.button("Check Brand"):
        b = brand.lower()
        if b in APPROVED_BRANDS:
            st.success("Recognized brand — verify model BIS")
        elif b in DISAPPROVED_BRANDS:
            st.error("Avoid this brand")
        else:
            st.warning("Brand not listed — verify carefully")

# ==================================================
# ASSISTANT
# ==================================================
elif st.session_state.page == "assistant":
    q = st.text_input("Ask your question")
    if st.button("Get Answer"):
        st.info("Always verify BIS mark and CM/L license")

# ==================================================
# COMPLAINT
# ==================================================
elif st.session_state.page == "complaint":
    st.markdown(
        "[🚨 Official BIS Complaint Portal](https://consumerapp.bis.gov.in)"
    )

# ==================================================
# FEEDBACK
# ==================================================
elif st.session_state.page == "feedback":
    fb = st.text_area("Your feedback")
    if st.button("Submit"):
        st.success("Thank you!")

# ==================================================
# FOOTER
# ==================================================
st.divider()
st.caption("Educational & awareness platform only. Not official BIS system.")
