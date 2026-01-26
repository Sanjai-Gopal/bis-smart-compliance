import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="BIS Consumer Safety Portal",
    layout="wide",
    page_icon="🛡️"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color:#0e1117; }
.block-container { padding-top:2rem; }
.success-box { background:#0f5132; padding:15px; border-radius:8px; color:white; }
.warn-box { background:#664d03; padding:15px; border-radius:8px; color:white; }
.error-box { background:#842029; padding:15px; border-radius:8px; color:white; }
.info-box { background:#0d6efd; padding:15px; border-radius:8px; color:white; }
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
VERIFIED_BRANDS = {
    "havells", "philips", "bajaj", "usha", "orient", "crompton",
    "godrej", "lg", "samsung", "sony", "panasonic", "bosch",
    "siemens", "whirlpool", "voltas", "blue star", "ifb",
    "onida", "haier", "hitachi", "mi", "xiaomi", "redmi",
    "asus", "dell", "hp", "lenovo", "acer", "realme",
    "boat", "noise", "jbl", "sony liv", "tata power",
    "luminous", "microtek", "v-guard", "syska", "wipro",
    "anchor", "schneider", "legrand", "polycab",
    "finolex", "cello", "prestige", "pigeon", "kent",
    "livpure", "aquaguard"
}

UNDER_VERIFICATION = {
    "nothing", "iqoo", "infinix", "tecno", "lava",
    "motorola", "oppo", "vivo", "oneplus nord",
    "realme narzo", "boAt pro"
}

DISAPPROVED = {
    "quickcharge pro", "powermax", "ultrafast",
    "supervolt", "megapower", "china power",
    "fastcharge x", "eco power plus"
}

# ---------------- HEADER ----------------
st.markdown("""
<div style="background:#0b1c3d;padding:25px;border-radius:12px;">
<h1 style="color:white;text-align:center;">🛡️ BIS Consumer Safety Portal</h1>
<p style="color:#dce3f0;text-align:center;">
Public platform for product safety awareness, brand verification & compliance guidance
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🔍 Product Safety Check",
        "🏷️ Brand & Model Lookup",
        "🤖 Consumer AI Assistant",
        "📢 Complaint & Help Desk",
        "ℹ️ About"
    ]
)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.subheader("Why this platform exists")
    st.write("""
    - Protect consumers from unsafe or misleading products  
    - Educate buyers about BIS standards  
    - Help identify fake certification claims  
    - Guide users to official complaint channels  
    """)

# ---------------- PRODUCT SAFETY ----------------
elif page == "🔍 Product Safety Check":
    st.subheader("🔍 Product Safety Check")
    text = st.text_area("Enter product claims", height=120)

    if st.button("Analyze"):
        if not text.strip():
            st.warning("Please enter product claims.")
        else:
            text_l = text.lower()
            results = []

            if any(x in text_l for x in ["shockproof", "electric", "charger", "heater"]):
                results.append("✔ Electrical safety claims require IS 13252 testing.")
            if "waterproof" in text_l:
                results.append("✔ Waterproof claims require IS 60529 (IP rating).")
            if "fire resistant" in text_l:
                results.append("✔ Fire resistance falls under IS 1646.")
            if "child safe" in text_l:
                results.append("✔ Child safety relates to IS 9873.")
            if "eco friendly" in text_l:
                results.append("⚠ 'Eco-friendly' is not officially defined by BIS.")
            if "bis certified" in text_l:
                results.append("⚠ BIS certification must include a valid CM/L license number.")

            if results:
                for r in results:
                    st.markdown(f"<div class='success-box'>{r}</div>", unsafe_allow_html=True)
            else:
                st.info("No regulated BIS claims detected.")

# ---------------- BRAND LOOKUP ----------------
elif page == "🏷️ Brand & Model Lookup":
    st.subheader("🏷️ Brand & Model Verification")

    brand = st.text_input("Enter Brand Name").lower().strip()
    model = st.text_input("Enter Model Number (optional)")

    if st.button("Search Brand"):
        if not brand:
            st.warning("Please enter a brand name.")
        elif brand in VERIFIED_BRANDS:
            st.markdown(
                f"<div class='success-box'>✅ <b>{brand.title()}</b> is a BIS-recognized brand.<br>Status: APPROVED</div>",
                unsafe_allow_html=True
            )
        elif brand in UNDER_VERIFICATION:
            st.markdown(
                f"<div class='warn-box'>🟡 <b>{brand.title()}</b> is under BIS verification.<br>Status: PENDING</div>",
                unsafe_allow_html=True
            )
        elif brand in DISAPPROVED:
            st.markdown(
                f"<div class='error-box'>❌ <b>{brand.title()}</b> is NOT approved by BIS.<br>Possible misleading claims.</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='info-box'>❓ Brand not found in demo registry.<br>Please verify manually on BIS portal.</div>",
                unsafe_allow_html=True
            )

# ---------------- AI ASSISTANT ----------------
elif page == "🤖 Consumer AI Assistant":
    st.subheader("🤖 Consumer AI Assistant")
    q = st.text_input("Ask a safety or compliance question")

    if st.button("Get Answer"):
        if not q.strip():
            st.warning("Please enter a question.")
        else:
            ql = q.lower()
            if "is 13252" in ql:
                st.info("IS 13252 defines safety requirements for electrical appliances.")
            elif "eco friendly" in ql:
                st.info("Eco-friendly claims are marketing terms and not formally defined under BIS.")
            elif "fake bis" in ql or "report" in ql:
                st.info("Fake BIS claims should be reported via the official BIS consumer portal.")
            else:
                st.info("This assistant provides general awareness. For official decisions, contact BIS.")

# ---------------- COMPLAINT ----------------
elif page == "📢 Complaint & Help Desk":
    st.subheader("📢 Official BIS Complaint Support")
    st.markdown("""
    For legal action or investigation, complaints must be filed through the official BIS portal.
    """)
    st.markdown(
        "[🔗 Go to Official BIS Consumer Complaint Portal](https://consumerapp.bis.gov.in)",
        unsafe_allow_html=True
    )

# ---------------- ABOUT ----------------
elif page == "ℹ️ About":
    st.subheader("About This Project")
    st.write("""
    - Educational & awareness platform  
    - Demonstrates consumer safety technology  
    - Not an official BIS system  
    - Built for public interest & academic evaluation  
    """)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<p style="text-align:center;color:gray;font-size:13px;">
Educational & awareness platform only. Not an official BIS system.
</p>
""", unsafe_allow_html=True)
