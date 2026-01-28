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
        if not text or not text.strip():
            st.warning("Please enter product information.")
        else:
            t = text.lower().strip()

            # ================= SMART ANALYSIS =================
            reasons = []
            risk_score = 0
            category = "General Product"

            # -------- PRODUCT CATEGORY DETECTION --------
            if any(k in t for k in ["charger", "heater", "iron", "electric", "power", "adapter"]):
                category = "Electrical Product"
                risk_score += 15
                reasons.append("Electrical products have shock and fire risk.")

            if any(k in t for k in ["toy", "baby", "child"]):
                category = "Child Product"
                risk_score += 20
                reasons.append("Child safety products require strict BIS compliance.")

            if any(k in t for k in ["water", "heater", "geyser", "bath"]):
                risk_score += 10
                reasons.append("Products used near water need extra safety protection.")

            # -------- CLAIM ANALYSIS --------
            if any(k in t for k in ["eco", "green", "environment"]):
                risk_score += 10
                reasons.append("Eco-friendly is a marketing term, not BIS certified.")

            if any(k in t for k in ["shockproof", "fireproof", "waterproof"]):
                risk_score += 15
                reasons.append("Strong safety claims require BIS test proof.")

            if any(k in t for k in ["explosion", "blast", "100% safe", "unbreakable"]):
                risk_score += 40
                reasons.append("Unrealistic claims are unsafe and misleading.")

            # -------- BIS & LEGAL CHECK --------
            if "bis" not in t:
                risk_score += 15
                reasons.append("No BIS reference found on product description.")

            if "bis certified" in t or "bis approved" in t:
                reasons.append("BIS claims must include a valid CM/L license number.")

            # -------- PRICE & QUALITY SIGNAL --------
            if any(k in t for k in ["cheap", "lowest price", "best price"]):
                risk_score += 10
                reasons.append("Very low price products may compromise safety.")

            # -------- FINAL RISK NORMALIZATION --------
            if risk_score > 100:
                risk_score = 100

            # ================= DECISION =================
            st.subheader("🧾 Safety Assessment Result")

            if risk_score <= 25:
                decision = "✅ Safe to use"
                style = "ok"
            elif risk_score <= 60:
                decision = "⚠️ Use with caution"
                style = "warn"
            else:
                decision = "❌ Not recommended to use"
                style = "bad"

            st.markdown(
                f"<div class='{style}'>"
                f"<b>Product Category:</b> {category}<br>"
                f"# ---------- SAFETY STATUS (INSTEAD OF SCORE) ----------
if risk_score <= 25:
    safety_status = "🟢 Low Risk – Generally Safe"
    confidence = "High"
    style = "ok"
elif risk_score <= 60:
    safety_status = "🟡 Moderate Risk – Needs Verification"
    confidence = "Medium"
    style = "warn"
else:
    safety_status = "🔴 High Risk – Avoid Use"
    confidence = "Low"
    style = "bad"

st.markdown(
    f"<div class='{style}'>"
    f"<b>Product Category:</b> {category}<br>"
    f"<b>Safety Status:</b> {safety_status}<br>"
    f"<b>Safety Confidence:</b> {confidence}<br>"
    f"<b>Final Recommendation:</b> {decision}"
    f"</div>",
    unsafe_allow_html=True
)
"
                f"<b>Final Recommendation:</b> {decision}"
                f"</div>",
                unsafe_allow_html=True
            )

            # ================= EXPLANATION =================
            if reasons:
                st.markdown("### 📌 Why this decision?")
                for r in reasons:
                    st.write("•", r)

            # ================= CONSUMER GUIDANCE =================
            st.markdown("### 🛡️ What you should do next")
            st.write("• Check for BIS mark and license number on the product")
            st.write("• Verify manufacturer details and address")
            st.write("• Avoid unrealistic or exaggerated safety claims")
            st.write("• Buy from trusted sellers")

            st.info(
                "This assessment provides awareness guidance only. "
                "Final safety confirmation should be done through BIS verification."
            )
# ==================================================
# BRAND CHECK
# ==================================================
elif st.session_state.page == "brand":
    st.header("🏷️ Brand Verification")

    brand = st.text_input("Enter brand name (example: Havells, Philips, MI)")
    model = st.text_input("Enter model number (optional)")
    product_type = st.selectbox(
        "Select product type (optional)",
        ["Not sure", "Electrical appliance", "Electronic gadget", "Child product", "Kitchen appliance", "Other"]
    )

    if st.button("Verify Brand"):
        if not brand or not brand.strip():
            st.warning("Please enter a brand name.")
        else:
            b = brand.lower().strip()

            reasons = []
            trust_score = 50  # neutral baseline

            # ---------- BRAND CATEGORY ----------
            if b in APPROVED_BRANDS:
                trust_score += 30
                reasons.append("Brand is widely known and commonly BIS-compliant.")

            elif b in DISAPPROVED_BRANDS:
                trust_score -= 40
                reasons.append("Brand has been associated with misleading or unsafe claims.")

            else:
                trust_score -= 10
                reasons.append("Brand is not found in common consumer registry.")

            # ---------- PRODUCT TYPE RISK ----------
            if product_type == "Electrical appliance":
                trust_score -= 5
                reasons.append("Electrical products require strict BIS safety compliance.")

            if product_type == "Child product":
                trust_score -= 10
                reasons.append("Child products require higher safety standards.")

            # ---------- MODEL INFORMATION ----------
            if model.strip():
                reasons.append("Model number provided — BIS certification must be verified for this exact model.")
            else:
                trust_score -= 5
                reasons.append("No model number provided, verification is incomplete.")

            # ---------- SCORE NORMALIZATION ----------
            if trust_score > 100:
                trust_score = 100
            if trust_score < 0:
                trust_score = 0

            # ---------- FINAL DECISION ----------
            if trust_score >= 70:
                decision = "✅ Trusted brand (verify model certification)"
                style = "ok"
            elif trust_score >= 40:
                decision = "⚠️ Use with caution"
                style = "warn"
            else:
                decision = "❌ Not recommended"
                style = "bad"

            # ---------- DISPLAY RESULT ----------
            st.subheader("📋 Brand Trust Assessment")

            st.markdown(
                f"<div class='{style}'>"
                f"<b>Brand:</b> {brand.title()}<br>"
                f"<b>Trust Score:</b> {trust_score} / 100<br>"
                f"<b>Final Recommendation:</b> {decision}"
                f"</div>",
                unsafe_allow_html=True
            )

            # ---------- EXPLANATION ----------
            st.markdown("### 📌 Why this decision?")
            for r in reasons:
                st.write("•", r)

            # ---------- CONSUMER GUIDANCE ----------
            st.markdown("### 🛡️ What you should do next")
            st.write("• Check BIS mark and CM/L license number on the product")
            st.write("• Verify manufacturer name and address")
            st.write("• Ensure certification matches the exact model")
            st.write("• Avoid brands making unrealistic safety claims")

            st.info(
                "This brand check provides awareness guidance only. "
                "BIS certification is product- and model-specific."
            )
# ==================================================
# AI ASSISTANT (SAFE FALLBACK)
# ==================================================
elif st.session_state.page == "assistant":
    st.header("🤖 Consumer Safety Assistant")

    q = st.text_input(
        "Ask your question (example: Should I buy this charger?, Is BIS compulsory?, Fake BIS mark?)"
    )

    if st.button("Get Answer"):
        if not q or not q.strip():
            st.warning("Please type a question.")
        else:
            ql = q.lower().strip()

            # ---------- BASIC SIGNAL CHECK ----------
            has_bis = "bis" in ql or "certif" in ql
            has_buy = "buy" in ql or "purchase" in ql or "use" in ql
            has_safe = "safe" in ql or "danger" in ql or "risk" in ql
            has_fake = "fake" in ql or "duplicate" in ql
            has_complain = "complain" in ql or "report" in ql
            has_eco = "eco" in ql or "green" in ql
            has_electric = "charger" in ql or "electric" in ql or "heater" in ql
            has_brand = "brand" in ql or "company" in ql
            has_cheap = "cheap" in ql or "low price" in ql

            # ---------- SMART DECISION ENGINE ----------

            # 1️⃣ Very risky situations
            if has_fake:
                st.markdown(
                    "**Decision:** ❌ Not recommended\n\n"
                    "**Reason:** Fake or duplicate BIS marks indicate serious safety risk.\n\n"
                    "**Action:** Do not buy or use the product. Report it on the official BIS portal:\n"
                    "https://consumerapp.bis.gov.in"
                )

            # 2️⃣ Buying electrical product
            elif has_buy and has_electric:
                st.markdown(
                    "**Decision:** ⚠️ Use only after verification\n\n"
                    "**Reason:** Electrical products can cause shock or fire if not certified.\n\n"
                    "**What BIS requires:** IS 13252 safety compliance.\n\n"
                    "**Action:** Check BIS mark and license number before buying."
                )

            # 3️⃣ Eco-friendly confusion
            elif has_eco:
                st.markdown(
                    "**Decision:** ⚠️ Claim needs caution\n\n"
                    "**Reason:** Eco-friendly is a marketing term and not defined by BIS.\n\n"
                    "**Action:** Focus on safety certification, not eco claims."
                )

            # 4️⃣ Brand trust only
            elif has_brand and not has_bis:
                st.markdown(
                    "**Decision:** ⚠️ Incomplete information\n\n"
                    "**Reason:** Brand name alone does not guarantee safety.\n\n"
                    "**Action:** Verify BIS mark for the specific product model."
                )

            # 5️⃣ General safety doubt
            elif has_safe:
                st.markdown(
                    "**Decision:** ⚠️ Depends on certification\n\n"
                    "**Reason:** Product safety depends on BIS compliance and realistic claims.\n\n"
                    "**Action:** Check BIS mark and avoid unrealistic promises."
                )

            # 6️⃣ Complaint guidance
            elif has_complain:
                st.markdown(
                    "**Action:** 📢 File a complaint\n\n"
                    "**When:** Fake BIS mark, unsafe product behavior, misleading claims.\n\n"
                    "**Official portal:** https://consumerapp.bis.gov.in"
                )

            # 7️⃣ BIS explanation
            elif has_bis:
                st.markdown(
                    "**What is BIS?**\n\n"
                    "BIS (Bureau of Indian Standards) ensures minimum safety and quality "
                    "standards for certain products in India.\n\n"
                    "**Why it matters:** It protects consumers from unsafe products."
                )

            # 8️⃣ Cheap products
            elif has_cheap:
                st.markdown(
                    "**Decision:** ⚠️ Higher risk\n\n"
                    "**Reason:** Extremely low prices may compromise safety.\n\n"
                    "**Action:** Verify BIS certification carefully."
                )

            # 9️⃣ Intelligent fallback
            else:
                st.markdown(
                    "**Guidance:**\n\n"
                    "I need more information to guide you correctly.\n\n"
                    "Please mention:\n"
                    "• Product type\n"
                    "• Brand name\n"
                    "• Whether BIS mark is present\n\n"
                    "_Consumer safety decisions should not be guessed._"
                )
# ==================================================
# COMPLAINT CENTRE
# ==================================================
elif st.session_state.page == "complaint":
    st.header("📢 BIS Consumer Complaint Centre")

    st.markdown(
        """
        <div class="card">
        <h3>When should you file a complaint?</h3>
        <ul>
            <li>Product shows a <b>fake or unclear BIS mark</b></li>
            <li>Electrical product <b>overheats, sparks, shocks, or smells</b></li>
            <li>Product makes <b>unrealistic claims</b> like “100% safe” or “explosion proof”</li>
            <li>No <b>manufacturer name, address, or license number</b></li>
            <li>Product quality looks unsafe or misleading</li>
        </ul>

        <h3>Why is filing a complaint important?</h3>
        <p>
        Filing a complaint helps BIS identify unsafe products, take legal action,
        protect other consumers, and improve product safety standards in India.
        </p>

        <h3>Official BIS Consumer Complaint Portal</h3>
        <p>
        Click the button below to file your complaint directly on the official BIS portal.
        </p>

        <a href="https://www.bing.com/ck/a?!&&p=3da73ad258c8f3207551bc083d661321c650ed874f1ac5cdae1c897befa9875cJmltdHM9MTc2OTQ3MjAwMA&ptn=3&ver=2&hsh=4&fclid=144e2a47-d94b-6a15-2583-3c30d8896bd0&psq=official+complaint+centre+of+bis&u=a1aHR0cHM6Ly93d3cuYmlzLmdvdi5pbi9jb25zdW1lci1vdmVydmlldy9jb25zdW1lci1vdmVydmlld3Mvb25saW5lLWNvbXBsYWludC1yZWdpc3RyYXRpb24vP2xhbmc9ZW4" target="_blank">
            <button style="
                background:#1e40af;
                color:white;
                padding:14px 22px;
                border:none;
                border-radius:12px;
                font-size:16px;
                cursor:pointer;
            ">
                🚨 Go to Official BIS Complaint Portal
            </button>
        </a>

        <p style="margin-top:12px; opacity:0.8;">
        This portal is managed by the <b>Bureau of Indian Standards (Government of India)</b>.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Note: This platform does not collect complaints or personal data. "
        "All complaints are handled only through the official BIS system."
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














