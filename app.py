import streamlit as st
import pandas as pd
import nltk

nltk.download("punkt")

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="BIS Smart Consumer Protection Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= DATA =================
bis_data = [
    {"claim": "shockproof", "bis_standard": "IS 13252", "status": "Needs Verification", "explanation": "Requires electrical safety testing"},
    {"claim": "waterproof", "bis_standard": "IS 60529", "status": "Needs Verification", "explanation": "IP rating required"},
    {"claim": "fire resistant", "bis_standard": "IS 1646", "status": "Regulated", "explanation": "Fire resistance standard"},
    {"claim": "energy efficient", "bis_standard": "IS 14800", "status": "Needs Verification", "explanation": "Star rating proof required"},
    {"claim": "eco friendly", "bis_standard": "N/A", "status": "Not Defined", "explanation": "Marketing claim – not defined by BIS"},
    {"claim": "child safe", "bis_standard": "IS 9873", "status": "Regulated", "explanation": "Toy safety standard"}
]
rules_df = pd.DataFrame(bis_data)

# ================= SIDEBAR (BRANDING) =================
st.sidebar.markdown("## 🏛️ BIS Smart Platform")
st.sidebar.markdown("**Consumer Safety • Compliance • Awareness**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Compliance Dashboard",
        "🧪 Testing Lab",
        "📢 Complaint Support",
        "📘 Consumer Awareness",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Public demo • Educational use")

# ================= HEADER =================
st.markdown("""
<div style="background-color:#0f172a;padding:25px;border-radius:12px;">
<h1 style="color:white;text-align:center;">BIS Smart Consumer Protection Platform</h1>
<p style="color:#cbd5e1;text-align:center;font-size:17px;">
AI-powered product safety verdict, trust scoring & official BIS complaint support
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# =====================================================
# 🏠 COMPLIANCE DASHBOARD
# =====================================================
if menu == "🏠 Compliance Dashboard":

    st.markdown("## 🔍 Product Compliance Analysis")

    product_text = st.text_area(
        "Enter product description",
        height=120,
        placeholder="Example: This appliance is shockproof, waterproof and energy efficient."
    )

    if st.button("🔎 Analyze Product", use_container_width=True):

        if product_text.strip() == "":
            st.warning("Please enter a product description.")
        else:
            detected = []
            for _, row in rules_df.iterrows():
                if row["claim"] in product_text.lower():
                    detected.append(row)

            if not detected:
                st.info("No BIS-related claims detected.")
            else:
                result_df = pd.DataFrame(detected)

                st.markdown("### 📋 Detected Claims")
                st.dataframe(
                    result_df[["claim", "bis_standard", "status", "explanation"]],
                    use_container_width=True
                )

                # ---------- TRUST SCORE ----------
                score = 0
                for s in result_df["status"]:
                    if s == "Regulated":
                        score += 30
                    elif s == "Needs Verification":
                        score += 15
                    else:
                        score += 5
                score = min(score, 100)

                undefined_claims = len(result_df[result_df["status"] == "Not Defined"])

                st.markdown("### 🤝 Product Trust Score")
                st.progress(score / 100)
                st.write(f"**Trust Score:** {score} / 100")

                # ---------- RISK ----------
                if score >= 70:
                    risk = "LOW"
                    risk_icon = "🟢"
                elif score >= 40:
                    risk = "MEDIUM"
                    risk_icon = "🟡"
                else:
                    risk = "HIGH"
                    risk_icon = "🔴"

                st.markdown(f"### 🚦 Risk Level: {risk_icon} **{risk}**")

                # ---------- AI VERDICT CARD ----------
                st.markdown("### 🧠 AI Safety Verdict")

                if risk == "HIGH":
                    verdict = "🔴 DO NOT BUY"
                    color = "#fee2e2"
                    steps = [
                        "Avoid purchasing this product",
                        "Check for fake BIS marking",
                        "Report product to BIS",
                        "Choose certified alternatives"
                    ]
                elif risk == "MEDIUM" or undefined_claims > 0:
                    verdict = "🟡 BUY WITH CAUTION"
                    color = "#fef9c3"
                    steps = [
                        "Ask seller for BIS certificate",
                        "Verify lab test / star rating",
                        "Buy only from trusted sellers"
                    ]
                else:
                    verdict = "🟢 SAFE TO BUY"
                    color = "#dcfce7"
                    steps = [
                        "Verify BIS mark on packaging",
                        "Keep invoice and warranty",
                        "Follow safety instructions"
                    ]

                st.markdown(f"""
                <div style="background-color:{color};padding:20px;border-radius:10px;">
                <h2 style="text-align:center;">{verdict}</h2>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 🧭 Recommended Actions")
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. {step}")

                if undefined_claims > 0:
                    st.warning("⚠️ This product uses marketing claims not officially defined by BIS.")

                with st.expander("🤖 Why did the system give this decision?"):
                    st.write("""
                    The decision is based on:
                    • BIS regulation coverage  
                    • Verification requirements  
                    • Presence of misleading claims  
                    • Overall trust score  
                    """)

# =====================================================
# 🧪 TESTING LAB
# =====================================================
elif menu == "🧪 Testing Lab":

    st.markdown("## 🧪 Product Testing Lab (For Judges)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Electrical Appliance**")
        st.code("This appliance is shockproof, waterproof and energy efficient.")

    with col2:
        st.markdown("**Misleading Product**")
        st.code("This product claims to be eco friendly and fire resistant without certification.")

    with col3:
        st.markdown("**Child Safety Product**")
        st.code("This toy is child safe and shockproof.")

# =====================================================
# 📢 COMPLAINT SUPPORT
# =====================================================
elif menu == "📢 Complaint Support":

    st.markdown("## 📢 Consumer Complaint Support")

    st.markdown("""
    This platform helps users identify unsafe or misleading products.  
    For **official action**, complaints must be filed through **BIS-authorized channels**.
    """)

    st.markdown("""
    <div style="background-color:#eff6ff;padding:20px;border-radius:10px;">
    <h3>🏛️ Official BIS Online Complaint Registration</h3>
    <p>
    Use the government-maintained BIS portal to register complaints related to
    product safety, misleading claims, or fake BIS certification.
    </p>
    <a href="https://www.bis.gov.in/consumer-overview/consumer-overviews/online-complaint-registration/?lang=en"
       target="_blank"
       style="font-size:16px;font-weight:bold;">
       🔗 Go to Official BIS Complaint Registration
    </a>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 📘 CONSUMER AWARENESS
# =====================================================
elif menu == "📘 Consumer Awareness":

    st.markdown("## 📘 Consumer Awareness & Safety")

    st.markdown("""
    ### Why BIS Compliance Matters
    - Protects consumer safety  
    - Prevents misleading claims  
    - Ensures minimum quality standards  

    ### Common Misleading Marketing Claims
    - “100% Eco Friendly”  
    - “Ultra Safe”  
    - “Certified” without BIS mark  

    ### What Consumers Should Do
    - Always check BIS certification  
    - Verify seller documents  
    - Report suspicious products  
    """)

# =====================================================
# ℹ️ ABOUT
# =====================================================
elif menu == "ℹ️ About":

    st.markdown("## ℹ️ About This Project")

    st.write("""
    **Project Name:** BIS Smart Consumer Protection Platform  
    **Domain:** Artificial Intelligence & Data Science  
    **Type:** Public-facing decision-support system  

    **Key Differentiators**
    - AI safety verdict (Buy / Caution / Do Not Buy)
    - Trust score and visual risk indicators
    - Consumer-centric action guidance
    - Direct redirection to official BIS complaint portal
    - Explainable AI decisions

    **Purpose:**  
    To empower consumers and support BIS objectives through technology.
    """)

# ================= FOOTER =================
st.markdown("---")
st.caption("⚖️ Disclaimer: This system is for educational and decision-support purposes only and does not replace official BIS certification.")
