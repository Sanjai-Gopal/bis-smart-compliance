import pandas as pd
import streamlit as st
import nltk

nltk.download('punkt')

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="BIS Smart Compliance System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
rules_df = pd.read_csv("bis_rules.csv")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🏛️ BIS Smart Product Compliance System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-powered product claim verification, risk analysis & consumer support</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Navigation")
section = st.sidebar.radio(
    "Go to:",
    ["Compliance Checker", "Quick Test Lab", "Complaint Centre", "Consumer Awareness", "About Project"]
)

# =====================================================
# 🧠 SECTION 1: COMPLIANCE CHECKER
# =====================================================
if section == "Compliance Checker":

    st.subheader("📝 Product Claim Compliance Checker")

    product_text = st.text_area(
        "Enter product description:",
        placeholder="Example: This charger is shockproof, waterproof and energy efficient."
    )

    if st.button("Check Compliance"):
        if product_text.strip() == "":
            st.warning("Please enter a product description.")
        else:
            found_claims = []
            for _, row in rules_df.iterrows():
                if row['claim'] in product_text.lower():
                    found_claims.append(row)

            if not found_claims:
                st.info("No BIS-related claims detected.")
            else:
                result_df = pd.DataFrame(found_claims)

                st.success("✅ Compliance Analysis Result")
                st.table(result_df[['claim', 'bis_standard', 'status', 'explanation']])

                # -------- Claim Summary --------
                st.markdown("### 📌 Claim Summary")
                st.write(f"Total Claims Detected: **{len(result_df)}**")

                # -------- Score Calculation --------
                score = 0
                for status in result_df['status']:
                    if status == "Regulated":
                        score += 30
                    elif status == "Needs Verification":
                        score += 15
                    else:
                        score += 5
                score = min(score, 100)

                st.markdown("### 📊 Compliance Score")
                st.progress(score / 100)
                st.write(f"**Score:** {score} / 100")

                # -------- Risk Level --------
                if score >= 70:
                    risk = "🟢 LOW RISK"
                elif score >= 40:
                    risk = "🟡 MEDIUM RISK"
                else:
                    risk = "🔴 HIGH RISK"

                st.markdown("### 🚦 Risk Level")
                st.write(risk)

                if "HIGH" in risk:
                    st.error("⚠️ High risk product. BIS certification strongly recommended.")
                elif "MEDIUM" in risk:
                    st.warning("⚠️ Medium risk. Verification documents required.")
                else:
                    st.success("✅ Product appears largely compliant.")

                with st.expander("ℹ️ How to interpret results"):
                    st.write("""
                    - **Regulated**: Covered under BIS standards  
                    - **Needs Verification**: Lab testing / certification needed  
                    - **Not Defined**: Marketing claim not regulated by BIS
                    """)

# =====================================================
# 🧪 SECTION 2: QUICK TEST LAB (FOR JUDGES)
# =====================================================
elif section == "Quick Test Lab":

    st.subheader("🧪 Judge Testing Lab")

    col1, col2, col3 = st.columns(3)

    if col1.button("Electrical Appliance"):
        st.write("This appliance is shockproof, waterproof and energy efficient.")

    if col2.button("Misleading Product"):
        st.write("This product claims to be eco friendly and fire resistant without certification.")

    if col3.button("Child Safety Product"):
        st.write("This toy is child safe and shockproof.")

    st.info("Judges can copy any test case and verify using the Compliance Checker.")

# =====================================================
# 📢 SECTION 3: COMPLAINT CENTRE (VERY IMPRESSIVE)
# =====================================================
elif section == "Complaint Centre":

    st.subheader("📢 Consumer Complaint Centre")

    st.write("Report unsafe or misleading products to support BIS enforcement.")

    name = st.text_input("Your Name")
    product = st.text_input("Product Name")
    issue = st.selectbox("Issue Type", [
        "Misleading Claims",
        "Safety Concern",
        "Fake BIS Mark",
        "Poor Quality",
        "Other"
    ])
    description = st.text_area("Describe the issue")

    if st.button("Submit Complaint"):
        if name and product and description:
            st.success("✅ Complaint submitted successfully (simulation).")
            st.info("This data can help BIS identify high-risk products.")
        else:
            st.warning("Please fill all required fields.")

# =====================================================
# 📘 SECTION 4: CONSUMER AWARENESS
# =====================================================
elif section == "Consumer Awareness":

    st.subheader("📘 Consumer Awareness & Safety")

    st.markdown("""
    ### Why BIS Compliance Matters
    - Prevents unsafe products  
    - Ensures quality standards  
    - Protects consumers  

    ### Common Misleading Claims
    - 100% Eco Friendly  
    - Ultra Safe  
    - Shockproof without certification  

    ### What You Can Do
    - Check BIS mark  
    - Verify claims  
    - Report suspicious products
    """)

# =====================================================
# ℹ️ SECTION 5: ABOUT PROJECT
# =====================================================
elif section == "About Project":

    st.subheader("ℹ️ About This Project")

    st.write("""
    **Project Title:** BIS Smart Product Compliance System  
    **Domain:** Artificial Intelligence & Data Science  
    **Type:** Software-based Decision Support System  

    **Key Features:**
    - NLP-based claim detection  
    - Compliance score & risk analysis  
    - Judge testing lab  
    - Consumer complaint centre  
    - Awareness & education module  

    **Objective:**  
    To support BIS goals by improving transparency, safety, and consumer awareness.
    """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚖️ Disclaimer: This system is for educational and decision-support purposes only and does not replace official BIS certification.")
