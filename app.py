import streamlit as st
import pandas as pd
import nltk

nltk.download("punkt")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="BIS Smart Consumer Protection Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- EMBEDDED BIS DATA ----------------
bis_data = [
    {"claim": "shockproof", "bis_standard": "IS 13252", "status": "Needs Verification", "explanation": "Requires electrical safety testing"},
    {"claim": "waterproof", "bis_standard": "IS 60529", "status": "Needs Verification", "explanation": "IP rating required"},
    {"claim": "fire resistant", "bis_standard": "IS 1646", "status": "Regulated", "explanation": "Fire resistance standard"},
    {"claim": "energy efficient", "bis_standard": "IS 14800", "status": "Needs Verification", "explanation": "Star rating proof required"},
    {"claim": "eco friendly", "bis_standard": "N/A", "status": "Not Defined", "explanation": "Marketing claim not defined by BIS"},
    {"claim": "child safe", "bis_standard": "IS 9873", "status": "Regulated", "explanation": "Toy safety standard"}
]

rules_df = pd.DataFrame(bis_data)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🏛️ BIS Smart Consumer Protection Platform</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>AI-powered safety verdict, trust score & official BIS complaint support</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Navigation")
section = st.sidebar.radio(
    "Select Section",
    [
        "Compliance Checker",
        "Quick Test Lab",
        "Complaint Centre",
        "Consumer Awareness",
        "About Project"
    ]
)

# =====================================================
# 🧠 SECTION 1: COMPLIANCE CHECKER
# =====================================================
if section == "Compliance Checker":

    st.subheader("📝 Product Compliance Checker")

    product_text = st.text_area(
        "Enter product description",
        placeholder="Example: This appliance is shockproof, waterproof and energy efficient."
    )

    if st.button("Analyze Product"):
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

                st.success("✅ Detected Claims & BIS Status")
                st.table(result_df[["claim", "bis_standard", "status", "explanation"]])

                # ---------------- TRUST SCORE ----------------
                score = 0
                for status in result_df["status"]:
                    if status == "Regulated":
                        score += 30
                    elif status == "Needs Verification":
                        score += 15
                    else:
                        score += 5
                score = min(score, 100)

                undefined_claims = len(result_df[result_df["status"] == "Not Defined"])

                st.markdown("### 🤝 Product Trust Score")
                st.progress(score / 100)
                st.write(f"**Trust Score:** {score} / 100")

                # ---------------- RISK LEVEL ----------------
                if score >= 70:
                    risk = "🟢 LOW RISK"
                elif score >= 40:
                    risk = "🟡 MEDIUM RISK"
                else:
                    risk = "🔴 HIGH RISK"

                st.markdown("### 🚦 Risk Level")
                st.write(risk)

                # ---------------- PRODUCT RISK LABEL ----------------
                st.markdown("### 🏷️ Product Risk Label")
                st.write("Safety Risk :", "🔴 HIGH" if "HIGH" in risk else "🟡 MEDIUM" if "MEDIUM" in risk else "🟢 LOW")
                st.write("Misleading Claim Risk :", "🟡 MEDIUM" if undefined_claims > 0 else "🟢 LOW")
                st.write("Compliance Risk :", "🔴 HIGH" if score < 40 else "🟡 MEDIUM" if score < 70 else "🟢 LOW")

                # ---------------- AI SAFETY VERDICT ----------------
                st.markdown("### 🧠 AI Safety Verdict")

                if "HIGH" in risk:
                    verdict = "🔴 DO NOT BUY"
                    steps = [
                        "Avoid purchasing this product",
                        "Check for fake BIS markings",
                        "Report the product to BIS",
                        "Choose a BIS-certified alternative"
                    ]
                elif "MEDIUM" in risk or undefined_claims > 0:
                    verdict = "🟡 BUY WITH CAUTION"
                    steps = [
                        "Ask seller for BIS certification",
                        "Verify safety and efficiency documents",
                        "Purchase only from trusted sellers"
                    ]
                else:
                    verdict = "🟢 SAFE TO BUY"
                    steps = [
                        "Check BIS mark on packaging",
                        "Keep invoice and warranty card",
                        "Follow safety instructions"
                    ]

                st.subheader(verdict)

                st.markdown("### 🧭 Customer Action Roadmap")
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. {step}")

                # ---------------- WARNINGS ----------------
                if undefined_claims > 0:
                    st.warning("⚠️ This product uses marketing claims not officially defined by BIS.")
                if "HIGH" in risk:
                    st.error("🚨 High safety risk detected. Consumer caution advised.")

                with st.expander("🤖 Why did the system give this verdict?"):
                    st.write("""
                    The verdict is based on:
                    • Number of regulated claims  
                    • Verification requirements  
                    • Presence of misleading marketing terms  
                    • Overall trust score
                    """)

# =====================================================
# 🧪 SECTION 2: QUICK TEST LAB
# =====================================================
elif section == "Quick Test Lab":

    st.subheader("🧪 Judge Testing Lab")

    col1, col2, col3 = st.columns(3)

    if col1.button("Electrical Appliance"):
        st.code("This appliance is shockproof, waterproof and energy efficient.")

    if col2.button("Misleading Product"):
        st.code("This product claims to be eco friendly and fire resistant without certification.")

    if col3.button("Child Safety Product"):
        st.code("This toy is child safe and shockproof.")

# =====================================================
# 📢 SECTION 3: COMPLAINT CENTRE
# =====================================================
elif section == "Complaint Centre":

    st.subheader("📢 Consumer Complaint Centre")

    st.write("Report unsafe or misleading products.")

    name = st.text_input("Your Name")
    product = st.text_input("Product Name")
    issue = st.selectbox(
        "Issue Type",
        ["Misleading Claims", "Safety Concern", "Fake BIS Mark", "Poor Quality", "Other"]
    )
    description = st.text_area("Describe the issue")

    if st.button("Submit Local Report"):
        if name and product and description:
            st.success("✅ Complaint recorded (demo system).")
        else:
            st.warning("Please fill all required fields.")

    st.markdown("### 🏛️ Official BIS Complaint Portal")
    st.write("For official action, file a complaint directly with BIS.")

    st.markdown(
        "[🔗 Click here to file complaint on official BIS portal](https://consumerbis.gov.in)",
        unsafe_allow_html=True
    )

# =====================================================
# 📘 SECTION 4: CONSUMER AWARENESS
# =====================================================
elif section == "Consumer Awareness":

    st.subheader("📘 Consumer Awareness & Safety")

    st.markdown("""
    **Why BIS Compliance Matters**
    - Prevents unsafe products  
    - Protects consumer rights  
    - Ensures minimum quality standards  

    **Common Misleading Claims**
    - 100% Eco Friendly  
    - Ultra Safe  
    - Certified without BIS mark  

    **What Consumers Should Do**
    - Always check BIS certification  
    - Verify seller documentation  
    - Report suspicious products
    """)

# =====================================================
# ℹ️ SECTION 5: ABOUT PROJECT
# =====================================================
elif section == "About Project":

    st.subheader("ℹ️ About This Project")

    st.write("""
    **Project Name:** BIS Smart Consumer Protection Platform  
    **Domain:** Artificial Intelligence & Data Science  
    **Type:** Software-based Decision Support System  

    **Unique Highlights**
    - AI-based safety verdict (Buy / Caution / Do Not Buy)
    - Trust score and product risk labeling
    - Consumer action roadmap
    - Official BIS complaint redirection
    - Explainable AI decisions

    **Goal:**  
    To empower consumers and support BIS objectives through technology.
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "⚖️ Disclaimer: This system is for educational and decision-support purposes only and does not replace official BIS certification."
)
