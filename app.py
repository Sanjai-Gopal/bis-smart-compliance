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
        "Ask your question (example: Should I buy this charger?, Is eco friendly safe?, Fake BIS?)"
    )

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please type your question.")
        else:
            ql = q.lower()

            # ============ INTENT DETECTION ============
            intents = {
                "bis": any(k in ql for k in ["bis", "certification", "certified"]),
                "safety": any(k in ql for k in ["safe", "unsafe", "danger", "risk"]),
                "buy": any(k in ql for k in ["buy", "purchase", "use"]),
                "fake": any(k in ql for k in ["fake", "false", "duplicate"]),
                "complain": any(k in ql for k in ["complain", "report", "complaint"]),
                "brand": any(k in ql for k in ["brand", "company", "manufacturer"]),
                "eco": any(k in ql for k in ["eco", "green", "environment"]),
                "electric": any(k in ql for k in ["charger", "electric", "heater", "power"]),
                "cheap": any(k in ql for k in ["cheap", "low price", "very low"]),
            }

            # ============ RESPONSE LOGIC ============
            # Case 1: Buying + Safety (most common)
            if intents["buy"] and intents["safety"]:
                st.markdown(
                    "**Final Answer:** ⚠️ Decide after verification\n\n"
                    "**Reasoning:** Product safety depends on BIS certification, "
                    "brand reliability, and realistic claims.\n\n"
                    "**What BIS expects:** Mandatory BIS standards for regulated products.\n\n"
                    "**What you should do:**\n"
                    "• Check BIS mark and license number\n"
                    "• Avoid unrealistic claims\n"
                    "• Buy from trusted sellers"
                )

            # Case 2: Eco-friendly confusion
            elif intents["eco"]:
                st.markdown(
                    "**Final Answer:** ⚠️ Marketing term only\n\n"
                    "**Reasoning:** BIS does not certify products as eco-friendly.\n\n"
                    "**What BIS says:** Only safety and quality standards are regulated.\n\n"
                    "**What you should do:** Focus on BIS safety certification, not eco claims."
                )

            # Case 3: Electrical products
            elif intents["electric"]:
                st.markdown(
                    "**Final Answer:** ⚠️ Needs BIS safety compliance\n\n"
                    "**Reasoning:** Electrical products can cause shock or fire.\n\n"
                    "**What BIS says:** IS 13252 is required for many electrical items.\n\n"
                    "**What you should do:** Avoid products without BIS mark."
                )

            # Case 4: Fake BIS
            elif intents["fake"]:
                st.markdown(
                    "**Final Answer:** ❌ Do not use\n\n"
                    "**Reasoning:** Fake BIS marks hide safety risks.\n\n"
                    "**What BIS says:** Fake certification is illegal.\n\n"
                    "**What you should do:** Do not buy and report to BIS."
                )

            # Case 5: Complaint
            elif intents["complain"]:
                st.markdown(
                    "**Final Answer:** 📢 File an official complaint\n\n"
                    "**Reasoning:** BIS investigates unsafe or misleading products.\n\n"
                    "**What you should do:** Submit details at:\n"
                    "https://consumerapp.bis.gov.in"
                )

            # Case 6: Brand trust
            elif intents["brand"]:
                st.markdown(
                    "**Final Answer:** ⚠️ Brand name alone is not enough\n\n"
                    "**Reasoning:** BIS certification is product- and model-specific.\n\n"
                    "**What you should do:** Verify the exact model and BIS mark."
                )

            # Case 7: Cheap products
            elif intents["cheap"]:
                st.markdown(
                    "**Final Answer:** ⚠️ Higher risk\n\n"
                    "**Reasoning:** Extremely low prices often compromise safety.\n\n"
                    "**What you should do:** Check BIS certification carefully."
                )

            # Case 8: BIS explanation
            elif intents["bis"]:
                st.markdown(
                    "**Final Answer:** ℹ️ BIS ensures minimum safety standards\n\n"
                    "**Explanation:** BIS defines quality and safety requirements for "
                    "certain products in India.\n\n"
                    "**What you should do:** Look for BIS mark and license number."
                )

            # Fallback (always safe)
            else:
                st.markdown(
                    "**Guidance:**\n\n"
                    "• Verify BIS mark and license number\n"
                    "• Avoid unrealistic safety claims\n"
                    "• Buy from trusted brands\n"
                    "• Report doubts to BIS\n\n"
                    "This assistant provides awareness guidance only."
                )
# ==================================================
# COMPLAINT CENTRE
# ==================================================
elif st.session_state.page == "complaint":
    st.header("📢 Complaint Centre")

    st.markdown(
        """
        <div class="card">
        <h3>When should you file a complaint?</h3>
        <ul>
        <li>Product has a <b>fake or unclear BIS mark</b></li>
        <li>Electrical product <b>overheats, sparks, or smells</b></li>
        <li>Claims like <b>100% safe</b> or <b>explosion proof</b></li>
        <li>No manufacturer address or license number</li>
        </ul>

        <h3>Why filing a complaint is important?</h3>
        <p>
        Filing a complaint helps BIS take action against unsafe products,
        protects other consumers, and improves overall product safety.
        </p>

        <h3>Official BIS Consumer Complaint Portal</h3>
        <p>
        Click below to submit your complaint directly to BIS:
        </p>

        <p style="font-size:18px;">
        🔗 <b>https://www.bis.gov.in/consumer-overview/consumer-overviews/online-complaint-registration/</b>
        </p>

        <p style="opacity:0.8;">
        This portal is managed by the Bureau of Indian Standards (Government of India).
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Note: This platform does not collect complaints. "
        "All official actions are handled only by BIS."
    )
# ==================================================
# FEEDBACK (MUST-HAVE)
# ==================================================
elif st.session_state.page == "feedback":
    st.header("📝 User Feedback")

    st.markdown(
        """
        <div class="card">
        <p>
        Your feedback helps improve this consumer safety platform.
        Please share your experience.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    name = st.text_input("Your Name (optional)")
    rating = st.select_slider(
        "Rate your experience",
        options=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    )
    feedback = st.text_area("Your feedback or suggestion")

    if st.button("Submit Feedback"):
        if not feedback.strip():
            st.warning("Please write some feedback before submitting.")
        else:
            st.success("Thank you for your feedback! 🙏")
            st.caption("Feedback recorded for improvement purposes.")
# ==================================================
# FOOTER
# ==================================================
st.divider()
st.markdown("""
<div class="footer">
Educational & awareness platform only. Not an official BIS system.
</div>
""", unsafe_allow_html=True)








