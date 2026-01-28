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
/* ================= GLOBAL ================= */
body {
  background-color: #0b1220;
}

/* ================= ANIMATIONS ================= */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes glow {
  0% { box-shadow: 0 0 0px rgba(59,130,246,0.2); }
  50% { box-shadow: 0 0 18px rgba(59,130,246,0.35); }
  100% { box-shadow: 0 0 0px rgba(59,130,246,0.2); }
}

/* ================= HERO ================= */
.hero {
  background: linear-gradient(135deg, #0b3c8c, #081f4d);
  padding: 40px;
  border-radius: 22px;
  color: white;
  text-align: center;
  animation: fadeUp 0.9s ease;
}

/* ================= CARDS ================= */
.card {
  background: #111827;
  padding: 24px;
  border-radius: 18px;
  margin-bottom: 22px;
  animation: fadeUp 0.6s ease;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Micro-interaction (premium feel) */
.card:hover {
  transform: scale(1.015);
  box-shadow: 0 10px 28px rgba(0,0,0,0.45);
}

/* ================= STATUS BLOCKS ================= */
.ok {
  background: linear-gradient(135deg, #14532d, #166534);
  padding: 16px;
  border-radius: 12px;
  color: white;
  animation: glow 3s infinite;
}

.warn {
  background: linear-gradient(135deg, #78350f, #92400e);
  padding: 16px;
  border-radius: 12px;
  color: white;
}

.bad {
  background: linear-gradient(135deg, #7f1d1d, #991b1b);
  padding: 16px;
  border-radius: 12px;
  color: white;
}

/* ================= BUTTONS ================= */
button {
  border-radius: 14px !important;
  font-weight: 600 !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}

/* ================= FOOTER ================= */
.footer {
  text-align: center;
  opacity: 0.75;
  font-size: 14px;
  margin-top: 10px;
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
# ==================================================
# PRODUCT SAFETY CHECK (FINAL – SMART & BIS-ALIGNED)
# ==================================================
elif st.session_state.page == "safety":
    st.header("🔍 Product Safety Check")

    st.caption(
        "Enter what is written on the product, box, or online description. "
        "Simple English is enough."
    )

    text = st.text_area(
        "Example: child safe toy, eco friendly charger, waterproof speaker"
    )

    if st.button("Analyze Safety"):
        if not text or not text.strip():
            st.warning("Please enter product information.")
            st.stop()

        t = text.lower().strip()

        # ================= DEFAULT STATE =================
        category = "General Consumer Product"
        safety_status = "🟢 Generally Safe"
        confidence = "High"
        recommendation = "Safe to use after basic verification"
        style = "ok"

        reasons = []
        bis_references = []

        # ================= PRODUCT CATEGORY DETECTION =================
        if any(k in t for k in ["charger", "adapter", "heater", "iron", "electric"]):
            category = "Electrical Product"
            safety_status = "🟡 Needs Verification"
            confidence = "Medium"
            recommendation = "Use with caution"
            style = "warn"
            reasons.append(
                "Electrical products may cause shock or fire if not certified."
            )
            bis_references.append("IS 13252 – Electrical safety standard")

        if any(k in t for k in ["toy", "child", "baby", "kids"]):
            category = "Child-related Product"
            safety_status = "🟡 Needs Verification"
            confidence = "Medium"
            recommendation = "Use only after verification"
            style = "warn"
            reasons.append(
                "Products used by children require strict safety compliance."
            )
            bis_references.append("IS 9873 – Safety of toys and child products")

        if any(k in t for k in ["waterproof", "water resistant", "ip rating"]):
            safety_status = "🟡 Needs Verification"
            confidence = "Medium"
            recommendation = "Verify waterproof certification before use"
            style = "warn"
            reasons.append(
                "Waterproof claims must be supported by certified IP ratings."
            )
            bis_references.append("IS 60529 – IP protection standards")

        # ================= CLAIM ANALYSIS =================
        if any(k in t for k in ["eco", "green", "environment friendly"]):
            reasons.append(
                "‘Eco-friendly’ is a marketing term and not defined under BIS certification."
            )

        if any(k in t for k in ["100% safe", "explosion proof", "unbreakable"]):
            safety_status = "🔴 High Risk"
            confidence = "Low"
            recommendation = "Not recommended until verified"
            style = "bad"
            reasons.append(
                "Unrealistic safety claims are misleading and unsafe."
            )

        # ================= BIS MARK CHECK =================
        if "bis" not in t:
            if safety_status == "🟢 Generally Safe":
                safety_status = "🟡 Needs Verification"
                confidence = "Medium"
                recommendation = "Verify BIS mark before use"
                style = "warn"
            reasons.append(
                "No BIS mark or license reference mentioned in the product description."
            )
        else:
            reasons.append(
                "BIS claim detected. Verify the CM/L license number on the product."
            )

        # ================= DISPLAY RESULT =================
        st.markdown(
            f"""
            <div class="{style}">
            <h3>Safety Assessment Result</h3>

            <b>Detected Product Category:</b> {category}<br><br>

            <b>Safety Status:</b> {safety_status}<br>
            <b>Confidence Level:</b> {confidence}<br><br>

            <b>Final Recommendation:</b><br>
            {recommendation}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ================= EXPLANATION =================
        if reasons:
            st.markdown("### 📌 Why this result?")
            for r in reasons:
                st.write("•", r)

        # ================= BIS REFERENCES =================
        if bis_references:
            st.markdown("### 📜 Relevant BIS Safety References (Awareness)")
            for ref in set(bis_references):
                st.write("•", ref)

        # ================= CONSUMER BENEFITS =================
        st.markdown("### 🛡️ How this helps consumers")
        st.write("✔ Avoids misleading safety claims")
        st.write("✔ Encourages BIS verification before purchase")
        st.write("✔ Protects children and families")
        st.write("✔ Reduces risk of electrical accidents")
        st.write("✔ Helps users with simple English understand safety")
        st.write("✔ Promotes informed buying decisions")

        # ================= NEXT STEPS =================
        st.markdown("### 👉 Recommended Next Steps")
        st.write("• Check BIS mark and CM/L license number on the product")
        st.write("• Verify manufacturer name and address")
        st.write("• Avoid products with exaggerated claims")
        st.write("• Report suspicious products to BIS if needed")

        st.info(
            "This safety assessment provides consumer awareness guidance only. "
            "Final safety confirmation must be done through official BIS verification."
        )
# ==================================================
# BRAND CHECK (FINAL – COMPLIANCE BASED, NO SCORE)
# ==================================================
elif st.session_state.page == "brand":
    st.header("🏷️ Brand & Model Compliance Check")

    brand = st.text_input("Enter Brand Name (example: Samsung, Havells, Philips)")
    model = st.text_input("Enter Model Number (optional)")

    product_type = st.selectbox(
        "Select Product Type (optional)",
        [
            "Not sure",
            "Electrical appliance",
            "Electronic accessory (charger, adapter)",
            "Child product / Toy",
            "Kitchen appliance",
            "Other"
        ]
    )

    if st.button("Check Compliance"):
        if not brand.strip():
            st.warning("Please enter a brand name.")
        else:
            b = brand.lower().strip()

            # ==================================================
            # BRAND RECOGNITION
            # ==================================================
            if b in APPROVED_BRANDS:
                brand_status = "🟢 Widely recognized Indian brand"
                brand_note = (
                    "This brand is commonly found in BIS-certified products. "
                    "However, BIS certification is issued per product model."
                )
                style = "ok"

            elif b in DISAPPROVED_BRANDS:
                brand_status = "🔴 Brand linked to misleading or unsafe claims"
                brand_note = (
                    "This brand has been reported for unsafe or misleading practices. "
                    "Consumers are strongly advised to avoid such products."
                )
                style = "bad"

            else:
                brand_status = "🟡 Brand not found in common consumer registry"
                brand_note = (
                    "This brand may be new or less documented. "
                    "Careful verification is required before purchase."
                )
                style = "warn"

            # ==================================================
            # PRODUCT TYPE → BIS STANDARD
            # ==================================================
            if product_type == "Electrical appliance":
                bis_rule = "IS 13252 – Electrical safety standard"
                risk_note = "Risk of electric shock or fire if the product is uncertified."

            elif product_type == "Electronic accessory (charger, adapter)":
                bis_rule = "IS 13252 – Safety of chargers and adapters"
                risk_note = "Overheating and electrical hazard risk if uncertified."

            elif product_type == "Child product / Toy":
                bis_rule = "IS 9873 – Safety requirements for toys"
                risk_note = "High safety requirement due to child usage."

            elif product_type == "Kitchen appliance":
                bis_rule = "IS 302 – Safety of household electrical appliances"
                risk_note = "Fire and electrical risk if BIS standards are not met."

            else:
                bis_rule = "Applicable BIS standard depends on the exact product category"
                risk_note = "Exact safety rule must be confirmed."

            # ==================================================
            # MODEL-LEVEL INSIGHT
            # ==================================================
            if model.strip():
                model_note = (
                    f"The model you entered (<b>{model}</b>) must have its "
                    "<b>own BIS CM/L license</b>.<br><br>"
                    "Important points:<br>"
                    "• BIS certification is issued per product model<br>"
                    "• Brand name alone does not guarantee safety<br>"
                    "• Always verify the BIS mark and license number on the product"
                )
            else:
                model_note = (
                    "No model number provided.<br><br>"
                    "For accurate verification:<br>"
                    "• Check the exact model printed on the product<br>"
                    "• BIS certification is always model-specific"
                )

            # ==================================================
            # COMPLIANCE VERDICT
            # ==================================================
            if b in DISAPPROVED_BRANDS:
                compliance_verdict = "❌ NON-COMPLIANT (High Consumer Risk)"
                final_guidance = "Avoid purchasing this product."

            elif b in APPROVED_BRANDS and model.strip():
                compliance_verdict = "⚠️ CONDITIONALLY COMPLIANT"
                final_guidance = (
                    "You may consider this brand, but verify the model’s BIS license "
                    "before purchase."
                )

            elif b in APPROVED_BRANDS:
                compliance_verdict = "⚠️ BRAND RECOGNIZED – MODEL NOT VERIFIED"
                final_guidance = (
                    "Brand is recognized, but model-level BIS verification is required."
                )

            else:
                compliance_verdict = "⚠️ COMPLIANCE STATUS UNKNOWN"
                final_guidance = (
                    "Proceed only after careful BIS verification."
                )

            # ==================================================
            # DISPLAY RESULT
            # ==================================================
            st.markdown(
                f"""
                <div class="{style}">
                <h3>Compliance Verdict</h3>
                <b>{compliance_verdict}</b><br><br>

                <b>Brand Recognition:</b> {brand_status}<br><br>

                <b>Brand Insight:</b><br>
                {brand_note}<br><br>

                <b>Detected Product Type:</b> {product_type}<br>
                <b>Applicable BIS Safety Rule:</b> {bis_rule}<br>
                <b>Consumer Risk:</b> {risk_note}<br><br>

                <b>Model-Level Insight:</b><br>
                {model_note}<br><br>

                <b>Final Consumer Guidance:</b><br>
                {final_guidance}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                "This result provides consumer awareness guidance only. "
                "Final confirmation must be done using the official BIS license database."
            )
# ==================================================
# AI ASSISTANT (SAFE FALLBACK)
# ==================================================
elif st.session_state.page == "assistant":
    st.header("🤖 Consumer Safety Assistant")

    st.caption(
        "Ask in simple English. Example: "
        "Is Samsung BIS certified? | "
        "Should I buy this charger? | "
        "What if BIS mark is fake?"
    )

    q = st.text_input("Ask your question")

    if st.button("Get Answer"):
        if not q or len(q.strip()) < 3:
            st.info(
                "Please ask a complete question. "
                "Example: Is Samsung charger BIS certified?"
            )
            st.stop()

        ql = q.lower()

        # ================= INTENT DETECTION =================
        asking_brand = any(w in ql for w in ["samsung", "lg", "philips", "mi", "sony", "havells"])
        asking_bis = "bis" in ql or "certif" in ql
        asking_buy = any(w in ql for w in ["buy", "purchase", "use"])
        asking_fake = "fake" in ql or "duplicate" in ql
        asking_charger = "charger" in ql or "adapter" in ql
        asking_child = "child" in ql or "baby" in ql
        asking_safe = "safe" in ql or "danger" in ql or "risk" in ql
        asking_complaint = "complain" in ql or "report" in ql

        # ================= SMART RESPONSES =================

        # 1️⃣ Brand + BIS question (MOST IMPORTANT)
        if asking_brand and asking_bis:
            st.markdown(
                """
                **Answer:**

                Popular brands like Samsung, LG, Philips, Havells and others
                **do manufacture BIS-certified products**, but **BIS certification
                is NOT for the brand — it is for each specific product model.**

                **What this means for consumers:**
                • One Samsung product may be BIS certified  
                • Another Samsung product may NOT be BIS certified  

                **What you must check:**
                ✔ BIS Standard Mark  
                ✔ CM/L license number  
                ✔ Product model matching the BIS record  

                **Conclusion:**  
                Do not trust the brand name alone. Always verify the BIS mark on the product.
                """
            )

        # 2️⃣ Buying electrical product
        elif asking_buy and asking_charger:
            st.markdown(
                """
                **Answer:**

                Chargers and electrical products can cause **electric shock,
                fire, or overheating** if not certified.

                **BIS Rule:**  
                Electrical products must comply with **IS 13252**.

                **Before buying, always check:**
                ✔ BIS mark on the product  
                ✔ License number (CM/L)  
                ✔ Manufacturer name and address  

                **Recommendation:**  
                Buy only after BIS verification.
                """
            )

        # 3️⃣ Fake BIS mark
        elif asking_fake:
            st.markdown(
                """
                **Answer:**

                A fake or duplicate BIS mark is a **serious safety risk**.

                **Why this is dangerous:**
                • Product is untested  
                • High risk of shock or fire  
                • Illegal under Indian law  

                **What you should do immediately:**
                ❌ Do NOT buy or use the product  
                📢 Report it on the official BIS portal  

                **Official complaint link:**  
                https://consumerapp.bis.gov.in
                """
            )

        # 4️⃣ Child safety questions
        elif asking_child:
            st.markdown(
                """
                **Answer:**

                Products used by children must follow **strict BIS child safety standards**.

                **Relevant BIS standard:**  
                IS 9873 (Safety of toys and child products)

                **Important note:**  
                Terms like *child safe* or *kids friendly* are **not BIS certifications**.

                **Recommendation:**  
                Verify BIS compliance carefully before allowing children to use the product.
                """
            )

        # 5️⃣ General safety question
        elif asking_safe:
            st.markdown(
                """
                **Answer:**

                Product safety depends on **certification, realistic claims,
                and manufacturing quality**.

                **General consumer safety rules:**
                • Check BIS mark  
                • Avoid exaggerated claims like *100% safe*  
                • Verify manufacturer details  

                **Conclusion:**  
                Safety should be verified — never assumed.
                """
            )

        # 6️⃣ Complaint guidance
        elif asking_complaint:
            st.markdown(
                """
                **Answer:**

                You should file a complaint if:
                • BIS mark looks fake  
                • Product overheats or sparks  
                • Misleading safety claims are used  

                **Official BIS Consumer Complaint Portal:**  
                https://consumerapp.bis.gov.in

                **Your complaint helps protect other consumers.**
                """
            )

        # 7️⃣ BIS explanation (basic users)
        elif asking_bis:
            st.markdown(
                """
                **What is BIS?**

                BIS (Bureau of Indian Standards) is a Government of India body
                that ensures **minimum safety and quality standards** for products.

                **Why BIS matters:**
                • Prevents unsafe products  
                • Protects consumers  
                • Reduces accidents and fraud  

                **Always prefer BIS-certified products.**
                """
            )

        # 8️⃣ Intelligent fallback (REAL AI BEHAVIOR)
        else:
            st.markdown(
                """
                **I need a little more information to guide you correctly.**

                Please try adding:
                • Product type (charger, toy, appliance)  
                • Brand name  
                • BIS mark present or not  

                **Example:**  
                *Is this Samsung charger BIS certified?*
                """
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

        <a href="https://www.bis.gov.in/consumer-overview/consumer-overviews/online-complaint-registration/?lang=en>
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
































