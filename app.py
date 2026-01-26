import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="BIS Consumer Safety Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SAMPLE BIS BRAND DATABASE (DEMO) =================
brand_data = [
    {"brand": "Philips", "model": "HL7756", "category": "Electrical Appliance", "status": "Verified"},
    {"brand": "Havells", "model": "Adonia-R", "category": "Electrical Appliance", "status": "Verified"},
    {"brand": "Syska", "model": "SSK-Power", "category": "Electrical Appliance", "status": "Under Verification"},
    {"brand": "LocalBrandX", "model": "EcoPlus-200", "category": "Electrical Appliance", "status": "Not Verified"},
    {"brand": "UnknownCo", "model": "FireSafe-Z", "category": "Home Appliance", "status": "Disapproved"}
]
brand_df = pd.DataFrame(brand_data)

# ================= SIDEBAR =================
st.sidebar.markdown("## 🏛️ BIS Consumer Safety Portal")
st.sidebar.markdown("Protect • Verify • Report")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🔍 Product Safety Check",
        "🏷️ Brand & Model Lookup",
        "🤖 Consumer AI Assistant",
        "📘 Consumer Guidance",
        "📢 Complaint & Help Desk",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Public awareness • Demo platform")

# ================= HEADER =================
st.markdown("""
<div style="background:#020617;padding:30px;border-radius:14px;">
<h1 style="color:white;text-align:center;">BIS Consumer Safety Portal</h1>
<p style="color:#cbd5f5;text-align:center;">
A public-facing platform for consumer safety awareness & compliance guidance
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# =====================================================
# 🏠 HOME
# =====================================================
if menu == "🏠 Home":
    st.markdown("## 👋 Welcome")

    st.write("""
    This platform helps consumers understand **product safety claims,
    brand reliability, and official BIS procedures**.

    It does **not certify products**, but guides users toward
    **informed decisions and official channels**.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Sample Brands Listed", len(brand_df))
    col2.metric("Verification Categories", "4")
    col3.metric("Official BIS Link", "Available")

# =====================================================
# 🔍 PRODUCT SAFETY CHECK
# =====================================================
elif menu == "🔍 Product Safety Check":
    st.markdown("## 🔍 Product Safety Check")
    st.info("Enter claims as shown on packaging or advertisements.")

    text = st.text_area("Product Description")

    if st.button("Analyze"):
        if "eco" in text.lower():
            st.warning("⚠️ 'Eco-friendly' is not officially defined under BIS.")
        if "shockproof" in text.lower():
            st.success("✔ Electrical safety claims require IS 13252 testing.")
        if text.strip() == "":
            st.info("No claims detected.")

# =====================================================
# 🏷️ BRAND & MODEL LOOKUP
# =====================================================
elif menu == "🏷️ Brand & Model Lookup":
    st.markdown("## 🏷️ Brand & Model Verification Lookup")

    brand = st.text_input("Enter Brand Name")
    model = st.text_input("Enter Model Number (optional)")

    if st.button("Search Brand"):

        results = brand_df[brand_df["brand"].str.lower() == brand.lower()]

        if model:
            results = results[results["model"].str.lower() == model.lower()]

        if results.empty:
            st.error("❌ Brand / Model not found in BIS demo registry.")
            st.caption("This does not mean the product is unsafe. Always verify through official BIS sources.")
        else:
            st.dataframe(results, use_container_width=True)

    st.caption("⚠️ Note: This is a demo registry. Real implementation requires official BIS datasets.")

# =====================================================
# 🤖 CONSUMER AI ASSISTANT
# =====================================================
elif menu == "🤖 Consumer AI Assistant":
    st.markdown("## 🤖 Consumer AI Assistant")
    st.write("Ask safety or compliance related questions.")

    question = st.text_input("Ask a question")

    if st.button("Get Answer"):
        q = question.lower()

        if "bis" in q:
            st.info("BIS is the Bureau of Indian Standards, responsible for product standardization and certification.")
        elif "complaint" in q:
            st.info("Consumers can file complaints through the official BIS online complaint registration portal.")
        elif "eco" in q:
            st.info("Eco-friendly claims are often marketing terms and not formally defined under BIS.")
        elif "safe" in q:
            st.info("Safety depends on certification, testing, and compliance with BIS standards.")
        elif question.strip() == "":
            st.warning("Please enter a question.")
        else:
            st.info("This assistant provides general guidance. For official decisions, contact BIS.")

# =====================================================
# 📘 CONSUMER GUIDANCE
# =====================================================
elif menu == "📘 Consumer Guidance":
    st.markdown("## 📘 Consumer Guidance")

    st.markdown("""
    ### Before Buying
    • Check BIS mark  
    • Verify brand authenticity  
    • Avoid exaggerated claims  

    ### After Buying
    • Keep invoice  
    • Register warranty  
    • Report unsafe products  

    ### Warning Signs
    • Fake BIS logo  
    • No manufacturer details  
    • Too-good-to-be-true claims
    """)

# =====================================================
# 📢 COMPLAINT & HELP DESK
# =====================================================
elif menu == "📢 Complaint & Help Desk":
    st.markdown("## 📢 Complaint & Help Desk")

    st.markdown("""
    <div style="background:#020617;padding:22px;border-radius:12px;">
    <h3 style="color:white;">🏛️ Official BIS Complaint Registration</h3>
    <p style="color:#cbd5f5;">
    Register product-related complaints through the official BIS portal.
    </p>
    <a href="https://www.bis.gov.in/consumer-overview/consumer-overviews/online-complaint-registration/?lang=en"
       target="_blank"
       style="font-size:17px;font-weight:bold;color:#38bdf8;">
       🔗 Go to BIS Online Complaint Registration
    </a>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# ℹ️ ABOUT
# =====================================================
elif menu == "ℹ️ About":
    st.markdown("## ℹ️ About This Platform")

    st.write("""
    This is a **consumer awareness and decision-support platform**
    built to demonstrate how AI can assist public safety systems.

    It does not replace BIS authority or certification.
    """)

# ================= FOOTER =================
st.markdown("---")
st.caption("⚖️ Disclaimer: Educational & awareness platform only. Not an official BIS system.")
