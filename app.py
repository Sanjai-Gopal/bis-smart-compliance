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
    {"claim": "shockproof", "bis_standard": "IS 13252", "status": "Needs Verification", "explanation": "Electrical safety testing required"},
    {"claim": "waterproof", "bis_standard": "IS 60529", "status": "Needs Verification", "explanation": "IP rating verification required"},
    {"claim": "fire resistant", "bis_standard": "IS 1646", "status": "Regulated", "explanation": "Fire resistance standard"},
    {"claim": "energy efficient", "bis_standard": "IS 14800", "status": "Needs Verification", "explanation": "BEE star rating required"},
    {"claim": "eco friendly", "bis_standard": "N/A", "status": "Not Defined", "explanation": "Marketing claim not defined by BIS"},
    {"claim": "child safe", "bis_standard": "IS 9873", "status": "Regulated", "explanation": "Toy safety standard"}
]
rules_df = pd.DataFrame(bis_data)

# ================= SIDEBAR =================
st.sidebar.markdown("## 🏛️ BIS Smart Platform")
st.sidebar.markdown("Consumer Safety • Compliance • Awareness")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate",
    [
        "📊 Compliance Dashboard",
        "🧪 Product Testing Lab",
        "📢 Official Complaint Support",
        "📘 Consumer Awareness",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Public demo • Educational use")

# ================= HEADER =================
st.markdown("""
<div style="background:#020617;padding:28px;border-radius:14px;">
<h1 style="color:white;text-align:center;">BIS Smart Consumer Protection Platform</h1>
<p style="color:#cbd5f5;text-align:center;font-size:16px;">
AI-powered product safety verdict, trust scoring & official BIS complaint support
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# =====================================================
# 📊 COMPLIANCE DASHBOARD
# =====================================================
if menu == "📊 Compliance Dashboard":

    st.markdown("## 🔍 Product Compliance Analysis")

    product_text = st.text_area(
        "Enter product description",
        height=120,
        placeholder="Example: This appliance is shockproof, waterproof and energy efficient."
    )

    if st.button("🔎 Analyze Product", use_container_width=True):

        detected = []
        for _, row in rules_df.iterrows():
            if row["claim"] in product_text.lower():
                detected.append(row)

        if not detected:
            st.info("No BIS-related claims detected.")
        else:
            df = pd.DataFrame(detected)

            # ---------- KPI CARDS ----------
            total_claims = len(df)
            regulated = len(df[df["status"] == "Regulated"])
            undefined = len(df[df["status"] == "Not Defined"])

            col1, col2, col3 = st.columns(3)
            col1.metric("Claims Detected", total_claims)
            col2.metric("Regulated Claims", regulated)
            col3.metric("Undefined Claims", undefined)

            st.markdown("### 📋 Compliance Details")
            st.dataframe(df, use_container_width=True)

            # ---------- TRUST SCORE ----------
            score = 0
            for s in df["status"]:
                score += 30 if s == "Regulated" else 15 if s == "Needs Verification" else 5
            score = min(score, 100)

            st.markdown("### 🤝 Trust Score")
            st.progress(score / 100)
            st.write(f"**{score} / 100**")

            # ---------- VERDICT ----------
            if score >= 70:
                verdict = "🟢 SAFE TO BUY"
                color = "#022c22"
            elif score >= 40:
                verdict = "🟡 BUY WITH CAUTION"
                color = "#3b2f00"
            else:
                verdict = "🔴 DO NOT BUY"
                color = "#450a0a"

            st.markdown(f"""
            <div style="background:{color};padding:20px;border-radius:10px;">
            <h2 style="text-align:center;color:white;">{verdict}</h2>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🤖 Why this verdict?"):
                st.write("""
                The verdict is generated using:
                • Number of regulated BIS claims  
                • Claims requiring verification  
                • Presence of undefined marketing terms  
                • Overall compliance confidence score
                """)

# =====================================================
# 🧪 PRODUCT TESTING LAB
# =====================================================
elif menu == "🧪 Product Testing Lab":

    st.markdown("## 🧪 Product Testing Lab (Judge Demo)")

    example = st.radio(
        "Choose a test case",
        [
            "Electrical Appliance",
            "Misleading Product",
            "Child Safety Product"
        ]
    )

    samples = {
        "Electrical Appliance": "This appliance is shockproof, waterproof and energy efficient.",
        "Misleading Product": "This product claims to be eco friendly and fire resistant without certification.",
        "Child Safety Product": "This toy is child safe and shockproof."
    }

    st.text_area("Test Input", samples[example], height=100)
    st.info("Judges can copy this text and test it in Compliance Dashboard.")

# =====================================================
# 📢 OFFICIAL COMPLAINT SUPPORT
# =====================================================
elif menu == "📢 Official Complaint Support":

    st.markdown("## 📢 Official BIS Complaint Support")

    st.markdown("""
    <div style="background:#020617;padding:22px;border-radius:12px;">
    <h3 style="color:white;">🏛️ Government of India – BIS Complaint Registration</h3>
    <p style="color:#cbd5f5;">
    If a product is unsafe, misleading, or falsely claims BIS certification,
    consumers must file complaints through the official BIS portal.
    </p>
    <a href="https://www.bis.gov.in/consumer-overview/consumer-overviews/online-complaint-registration/?lang=en"
       target="_blank"
       style="font-size:17px;font-weight:bold;color:#38bdf8;">
       🔗 Go to Official BIS Online Complaint Registration
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
    • Protects consumers from unsafe products  
    • Prevents misleading advertisements  
    • Ensures minimum quality standards  

    ### Common Misleading Claims
    • “100% Eco Friendly”  
    • “Ultra Safe”  
    • “Certified” without BIS mark  

    ### Consumer Responsibility
    • Check BIS certification  
    • Verify seller documents  
    • Report suspicious products
    """)

# =====================================================
# ℹ️ ABOUT PROJECT
# =====================================================
elif menu == "ℹ️ About Project":

    st.markdown("## ℹ️ About This Project")

    st.write("""
    **Project Name:** BIS Smart Consumer Protection Platform  
    **Domain:** Artificial Intelligence & Data Science  
    **Type:** Public-facing compliance decision system  

    **Key Strengths**
    • AI-generated safety verdict  
    • Trust scoring mechanism  
    • Official BIS complaint redirection  
    • Judge testing lab  
    • Consumer awareness integration  

    **Objective:**  
    To digitally support BIS goals and empower Indian consumers.
    """)

# ================= FOOTER =================
st.markdown("---")
st.caption("⚖️ Disclaimer: This system is for educational and decision-support purposes only and does not replace official BIS certification.")
