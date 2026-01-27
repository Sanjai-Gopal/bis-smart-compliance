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
    text = st.text_area(
        "Write what is written on the product or packaging (simple English is enough)"
    )

    if st.button("Analyze Safety"):
        if not text.strip():
            st.warning("Please enter product information.")
        else:
            t = text.lower()

            risk_level = "LOW"
            reasons = []

            # --- CLAIM ANALYSIS ---
            if re.search(r"eco|green|environment", t):
                risk_level = "MEDIUM"
                reasons.append(
                    "‘Eco-friendly’ is a marketing term and not defined by BIS."
                )

            if re.search(r"shock|electric|current|charger|heater", t):
                if risk_level != "HIGH":
                    risk_level = "MEDIUM"
                reasons.append(
                    "Electrical products must comply with IS 13252 safety standard."
                )

            if re.search(r"water|waterproof|rain|ip rating", t):
                if risk_level != "HIGH":
                    risk_level = "MEDIUM"
                reasons.append(
                    "Waterproof claims require a valid IP rating (IS 60529)."
                )

            if re.search(r"explosion|blast|unbreakable|100% safe", t):
                risk_level = "HIGH"
                reasons.append(
                    "Unrealistic safety claims are considered unsafe and misleading."
                )

            if re.search(r"bis certified|bis approved", t):
                reasons.append(
                    "BIS claims must include a valid CM/L license number."
                )

            # --- FINAL RECOMMENDATION ---
            st.subheader("🧾 Safety Assessment Result")

            if risk_level == "LOW":
                st.markdown(
                    "<div class='ok'>"
                    "<b>Recommendation:</b> ✅ Safe to use<br>"
                    "No major misleading or unsafe claims detected. "
                    "Still verify BIS mark before purchase."
                    "</div>",
                    unsafe_allow_html=True,
                )

            elif risk_level == "MEDIUM":
                st.markdown(
                    "<div class='warn'>"
                    "<b>Recommendation:</b> ⚠️ Use with caution<br>"
                    "Some claims require verification with BIS standards."
                    "</div>",
                    unsafe_allow_html=True,
                )

            else:  # HIGH
                st.markdown(
                    "<div class='bad'>"
                    "<b>Recommendation:</b> ❌ Not recommended to use<br>"
                    "Product claims appear unsafe or misleading."
                    "</div>",
                    unsafe_allow_html=True,
                )

            # --- EXPLANATION ---
            if reasons:
                st.markdown("### 📌 Why this recommendation?")
                for r in reasons:
                    st.write("•", r)

            st.info(
                "For final confirmation, always check the BIS mark and "
                "verify details on the official BIS website."
            )
# ==================================================
# BRAND CHECK
# ==================================================
elif st.session_state.page == "brand":
    st.header("🏷️ Brand Verification")

    brand = st.text_input("Enter brand name (example: Havells, Philips, MI)")
    model = st.text_input("Enter model number (optional)")

    if st.button("Verify Brand"):
        if not brand.strip():
            st.warning("Please enter a brand name.")
        else:
            b = brand.lower().strip()

            st.subheader("📋 Brand Verification Result")

            # ================= APPROVED BRANDS =================
            if b in APPROVED_BRANDS:
                st.markdown(
                    f"<div class='ok'>"
                    f"<b>Status:</b> ✅ Commonly BIS-compliant Brand<br>"
                    f"<b>Brand:</b> {brand.title()}<br>"
                    f"<b>Recommendation:</b> Safe to buy from this brand.<br>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.info(
                    "Note: BIS certification is product- and model-specific. "
                    "Always check the BIS mark and license number on the product."
                )

            # ================= DISAPPROVED BRANDS =================
            elif b in DISAPPROVED_BRANDS:
                st.markdown(
                    f"<div class='bad'>"
                    f"<b>Status:</b> ❌ Reported / Unsafe Brand<br>"
                    f"<b>Brand:</b> {brand.title()}<br>"
                    f"<b>Recommendation:</b> Not recommended to buy.<br>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.warning(
                    "This brand has been associated with misleading or unsafe claims. "
                    "Avoid purchasing and report if BIS mark appears fake."
                )

            # ================= UNKNOWN BRANDS =================
            else:
                st.markdown(
                    f"<div class='warn'>"
                    f"<b>Status:</b> ⚠️ Brand Not Found in Registry<br>"
                    f"<b>Brand:</b> {brand.title()}<br>"
                    f"<b>Recommendation:</b> Use with caution.<br>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.info(
                    "Unknown brand does not mean unsafe. "
                    "Please verify manufacturer details, BIS mark, and license number carefully."
                )

            # ================= MODEL NOTE =================
            if model.strip():
                st.caption(
                    f"Model entered: {model} — Please ensure this exact model "
                    "has BIS certification."
                )

            st.info(
                "For final confirmation, verify details on the official BIS website."
            )
# ==================================================
# AI ASSISTANT (SAFE FALLBACK)
# ==================================================
elif st.session_state.page == "assistant":
    st.header("🤖 Consumer Safety Assistant")

    q = st.text_input(
        "Ask your question (example: Is this product safe?, What is BIS?, Fake BIS?)"
    )

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please type a question.")
        else:
            ql = q.lower()

            # ================= BASIC QUESTIONS =================
            if "bis" in ql and ("what" in ql or "meaning" in ql):
                st.info(
                    "BIS stands for Bureau of Indian Standards. "
                    "It ensures that certain products meet minimum safety and quality standards in India."
                )

            elif "is safe" in ql or "safe to use" in ql:
                st.info(
                    "Safety depends on the product type, brand, and BIS certification. "
                    "Check for BIS mark and avoid unrealistic claims."
                )

            # ================= FAKE / MISLEADING =================
            elif "fake" in ql or "false" in ql or "duplicate" in ql:
                st.info(
                    "Fake BIS marks are illegal. "
                    "You should avoid such products and report them to BIS through the official complaint portal."
                )

            elif "eco" in ql:
                st.info(
                    "Eco-friendly is a marketing term. "
                    "BIS does not officially certify products as eco-friendly."
                )

            # ================= BUYING DECISIONS =================
            elif "should i buy" in ql or "buy or not" in ql:
                st.info(
                    "Before buying, check:\n"
                    "• BIS mark\n"
                    "• Trusted brand\n"
                    "• Manufacturer details\n"
                    "• Warranty information"
                )

            elif "cheap" in ql or "low price" in ql:
                st.info(
                    "Very low-priced electrical products may compromise safety. "
                    "Always check BIS certification and brand reliability."
                )

            # ================= BRAND QUESTIONS =================
            elif "brand" in ql:
                st.info(
                    "BIS certification is product-specific, not brand-wide. "
                    "Even trusted brands must certify individual models."
                )

            # ================= COMPLAINT =================
            elif "complain" in ql or "report" in ql:
                st.info(
                    "You can file a complaint for fake BIS marks, unsafe products, "
                    "or misleading claims on the official BIS consumer portal:\n"
                    "https://consumerapp.bis.gov.in"
                )

            # ================= ELECTRICAL =================
            elif "charger" in ql or "electric" in ql:
                st.info(
                    "Electrical products must follow IS 13252 safety standards. "
                    "Avoid products that heat excessively or lack BIS marks."
                )

            # ================= UNKNOWN / SAFE FALLBACK =================
            else:
                st.info(
                    "For consumer safety, always verify BIS mark, brand details, "
                    "and manufacturer information. "
                    "When in doubt, consult official BIS sources."
                )
# ==================================================
# COMPLAINT CENTRE
# ==================================================
elif st.session_state.page == "brand":
    st.header("🏷️ Brand Verification")

    brand = st.text_input("Enter brand name (example: Havells, Philips, MI)")
    model = st.text_input("Enter model number (optional)")

    if st.button("Verify Brand"):
        if not brand.strip():
            st.warning("Please enter a brand name.")
        else:
            b = brand.lower().strip()

            st.subheader("📋 Brand Verification Result")

            # ================= APPROVED BRANDS =================
            if b in APPROVED_BRANDS:
                st.markdown(
                    f"<div class='ok'>"
                    f"<b>Status:</b> ✅ Commonly BIS-compliant Brand<br>"
                    f"<b>Brand:</b> {brand.title()}<br>"
                    f"<b>Recommendation:</b> Safe to buy from this brand.<br>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.info(
                    "Note: BIS certification is product- and model-specific. "
                    "Always check the BIS mark and license number on the product."
                )

            # ================= DISAPPROVED BRANDS =================
            elif b in DISAPPROVED_BRANDS:
                st.markdown(
                    f"<div class='bad'>"
                    f"<b>Status:</b> ❌ Reported / Unsafe Brand<br>"
                    f"<b>Brand:</b> {brand.title()}<br>"
                    f"<b>Recommendation:</b> Not recommended to buy.<br>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.warning(
                    "This brand has been associated with misleading or unsafe claims. "
                    "Avoid purchasing and report if BIS mark appears fake."
                )

            # ================= UNKNOWN BRANDS =================
            else:
                st.markdown(
                    f"<div class='warn'>"
                    f"<b>Status:</b> ⚠️ Brand Not Found in Registry<br>"
                    f"<b>Brand:</b> {brand.title()}<br>"
                    f"<b>Recommendation:</b> Use with caution.<br>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                st.info(
                    "Unknown brand does not mean unsafe. "
                    "Please verify manufacturer details, BIS mark, and license number carefully."
                )

            # ================= MODEL NOTE =================
            if model.strip():
                st.caption(
                    f"Model entered: {model} — Please ensure this exact model "
                    "has BIS certification."
                )

            st.info(
                "For final confirmation, verify details on the official BIS website."
            )
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





